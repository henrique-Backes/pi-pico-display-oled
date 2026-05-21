import psutil
import platform
import os
import sys
import logging

logger = logging.getLogger(__name__)

_lhm_computer = None
_lhm_available = None

_detected_cpu_vendor = None
_detected_gpu_vendor = None

_CPU_VENDOR_LIBS: dict[str, list[str]] = {
    "Intel": ["lhm", "wmi", "psutil"],
    "AMD": ["lhm", "wmi", "psutil"],
    "Unknown": ["lhm", "wmi", "psutil"],
}

_GPU_VENDOR_LIBS: dict[str, list[str]] = {
    "NVIDIA": ["lhm", "pynvml"],
    "AMD": ["lhm", "pyadl"],
    "Intel": ["lhm"],
    "Unknown": ["lhm", "pynvml", "pyadl"],
}


def detect_cpu_vendor() -> str:
    """Detecta o fabricante da CPU (Intel, AMD ou Unknown).

    Tenta LibreHardwareMonitor primeiro para identificar pelo nome do hardware.
    Fallback para platform.processor() do Python.

    Returns:
        str: 'Intel', 'AMD' ou 'Unknown'.
    """
    global _detected_cpu_vendor

    if _detected_cpu_vendor is not None:
        return _detected_cpu_vendor

    lhm = _get_lhm()
    if lhm is not None:
        try:
            for hw in lhm.Hardware:
                if str(hw.HardwareType) == "Cpu":
                    name = (hw.Name or "").lower()
                    if "intel" in name:
                        _detected_cpu_vendor = "Intel"
                    elif "amd" in name:
                        _detected_cpu_vendor = "AMD"
                    else:
                        _detected_cpu_vendor = "Unknown"
                    return _detected_cpu_vendor
        except Exception:
            pass

    processor = platform.processor().lower()
    if "intel" in processor:
        _detected_cpu_vendor = "Intel"
    elif "amd" in processor:
        _detected_cpu_vendor = "AMD"
    else:
        _detected_cpu_vendor = "Unknown"

    return _detected_cpu_vendor


def detect_gpu_vendor() -> str:
    """Detecta o fabricante da GPU (NVIDIA, AMD, Intel ou Unknown).

    Tenta LibreHardwareMonitor primeiro para identificar pelo HardwareType.
    Fallback para WMI no Windows ou verificacao de libs disponiveis.

    Returns:
        str: 'NVIDIA', 'AMD', 'Intel' ou 'Unknown'.
    """
    global _detected_gpu_vendor

    if _detected_gpu_vendor is not None:
        return _detected_gpu_vendor

    lhm = _get_lhm()
    if lhm is not None:
        try:
            for hw in lhm.Hardware:
                hw_type = str(hw.HardwareType)
                if "Gpu" not in hw_type:
                    continue
                hw_type_lower = hw_type.lower()
                if "nvidia" in hw_type_lower:
                    _detected_gpu_vendor = "NVIDIA"
                elif "amd" in hw_type_lower:
                    _detected_gpu_vendor = "AMD"
                elif "intel" in hw_type_lower:
                    _detected_gpu_vendor = "Intel"
                else:
                    _detected_gpu_vendor = "Unknown"
                return _detected_gpu_vendor
        except Exception:
            pass

    try:
        import wmi

        w = wmi.WMI()
        for gpu in w.Win32_VideoController():
            name = (gpu.Name or "").lower()
            if "nvidia" in name:
                _detected_gpu_vendor = "NVIDIA"
            elif "amd" in name or "radeon" in name:
                _detected_gpu_vendor = "AMD"
            elif "intel" in name:
                _detected_gpu_vendor = "Intel"
            else:
                _detected_gpu_vendor = "Unknown"
            return _detected_gpu_vendor
    except Exception:
        pass

    _detected_gpu_vendor = "Unknown"
    return _detected_gpu_vendor


def detect_hardware() -> dict:
    """Executa a deteccao de fabricantes de CPU e GPU na inicializacao.

    Returns:
        dict: {'cpu_vendor': str, 'gpu_vendor': str, 'cpu_libs': list, 'gpu_libs': list}
    """
    cpu_v = detect_cpu_vendor()
    gpu_v = detect_gpu_vendor()
    return {
        "cpu_vendor": cpu_v,
        "gpu_vendor": gpu_v,
        "cpu_libs": _CPU_VENDOR_LIBS.get(cpu_v, _CPU_VENDOR_LIBS["Unknown"]),
        "gpu_libs": _GPU_VENDOR_LIBS.get(gpu_v, _GPU_VENDOR_LIBS["Unknown"]),
    }


def _get_lhm() -> object | None:
    """Inicializa e retorna a instancia do LibreHardwareMonitor (singleton).

    Returns:
        Computer object ou None se LHM nao estiver disponivel.
    """
    global _lhm_computer, _lhm_available

    if _lhm_available is False:
        return None

    if _lhm_computer is not None:
        return _lhm_computer

    try:
        import clr

        libs_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "libs")
        if libs_path not in sys.path:
            sys.path.append(libs_path)

        clr.AddReference("LibreHardwareMonitorLib")
        from LibreHardwareMonitor.Hardware import Computer

        _lhm_computer = Computer()
        _lhm_computer.IsCpuEnabled = True
        _lhm_computer.IsGpuEnabled = True
        _lhm_computer.Open()
        _lhm_available = True
        return _lhm_computer
    except Exception:
        _lhm_available = False
        return None


def get_cpu_info() -> dict:
    """Coleta dados da CPU e retorna no formato do protocolo JSON.

    Utiliza a cadeia de libs definida para o fabricante detectado.
    Cadeia padrao: LHM -> psutil.

    Returns:
        dict: Dicionario com chaves target, usage, temp, clock.
    """
    vendor = detect_cpu_vendor()
    libs = _CPU_VENDOR_LIBS.get(vendor, _CPU_VENDOR_LIBS["Unknown"])

    for lib in libs:
        if lib == "lhm":
            lhm = _get_lhm()
            if lhm is not None:
                info = _get_cpu_info_lhm(lhm)
                if info is not None:
                    return info
        elif lib == "wmi":
            info = _get_cpu_info_wmi()
            if info is not None:
                return info
        elif lib == "psutil":
            return _get_cpu_info_psutil()

    return _get_cpu_info_psutil()


def _get_cpu_info_lhm(lhm: object) -> dict | None:
    """Le dados da CPU via LibreHardwareMonitor.

    Args:
        lhm: Instancia Computer do LHM.

    Returns:
        dict ou None se falhar.
    """
    try:
        for hw in lhm.Hardware:
            if str(hw.HardwareType) == "Cpu":
                hw.Update()
                usage = 0.0
                temp = None
                clock = 0

                for s in hw.Sensors:
                    if s.Value is None:
                        continue
                    sname = s.Name.lower()
                    stype = str(s.SensorType)

                    if "total" in sname and stype == "Load":
                        usage = float(s.Value)
                    elif stype == "Temperature":
                        if "tctl" in sname or "tdie" in sname:
                            temp = float(s.Value)
                        elif temp is None:
                            temp = float(s.Value)
                    elif stype == "Clock":
                        if "core" in sname and "average" in sname and "effective" not in sname:
                            val = int(s.Value)
                            if val > 0 and val > clock:
                                clock = val

                for s in hw.Sensors:
                    if s.Value is None:
                        continue
                    stype = str(s.SensorType)
                    if stype == "Temperature" and (temp is None or s.Value > temp):
                        temp = float(s.Value)
                    if stype == "Clock" and s.Value > clock:
                        clock = int(s.Value)

        result_temp = round(temp if temp is not None else 0.0, 1)

        if result_temp == 0.0 and clock == 0:
            logger.debug("LHM CPU: temp e clock zerados, sem driver WinRing0?")
            return None

        return {
            "target": "CPU",
            "usage": round(usage, 1),
            "temp": result_temp,
            "clock": clock,
        }
    except Exception as e:
        logger.debug("Erro LHM CPU: %s", e)
        return None


def _get_cpu_info_wmi() -> dict | None:
    """Le dados da CPU via WMI (Win32_Processor).

    Funciona sem privilegios de admin. Fornece clock e usage,
    mas NAO fornece temperatura.

    Returns:
        dict ou None se WMI nao estiver disponivel.
    """
    try:
        import wmi as _wmi

        w = _wmi.WMI()
        cpu = w.Win32_Processor()
        if not cpu:
            return None

        processor = cpu[0]
        usage = float(processor.LoadPercentage or 0)
        clock = int(processor.CurrentClockSpeed or 0)

        return {
            "target": "CPU",
            "usage": round(usage, 1),
            "temp": 0.0,
            "clock": clock,
        }
    except Exception as e:
        logger.debug("Erro WMI CPU: %s", e)
        return None


def _get_cpu_info_psutil() -> dict:
    """Le dados da CPU via psutil (fallback).

    Returns:
        dict: Dados da CPU no formato do protocolo.
    """
    usage = psutil.cpu_percent(interval=1)
    cpu_freq = psutil.cpu_freq()
    clock = int(cpu_freq.current) if cpu_freq else 0

    temp = 0.0
    if hasattr(psutil, "sensors_temperatures"):
        temps = psutil.sensors_temperatures()
        if temps:
            for sensor_name in ("coretemp", "k10temp", "cpu_thermal", "acpitz"):
                if sensor_name in temps and len(temps[sensor_name]) > 0:
                    temp = float(temps[sensor_name][0].current)
                    break

    return {
        "target": "CPU",
        "usage": float(usage),
        "temp": temp,
        "clock": clock,
    }


def get_gpu_info() -> dict:
    """Coleta dados da GPU e retorna no formato do protocolo JSON.

    Utiliza a cadeia de libs definida para o fabricante detectado.
    NVIDIA: LHM -> pynvml
    AMD: LHM -> pyadl
    Intel: LHM
    Unknown: LHM -> pynvml -> pyadl

    Returns:
        dict: Dicionario com chaves target, usage, temp, vram_used, vram_total.
    """
    vendor = detect_gpu_vendor()
    libs = _GPU_VENDOR_LIBS.get(vendor, _GPU_VENDOR_LIBS["Unknown"])

    for lib in libs:
        if lib == "lhm":
            lhm = _get_lhm()
            if lhm is not None:
                info = _get_gpu_info_lhm(lhm)
                if info is not None:
                    return info
        elif lib == "pynvml":
            info = _get_gpu_info_pynvml()
            if info is not None:
                return info
        elif lib == "pyadl":
            info = _get_gpu_info_pyadl()
            if info is not None:
                return info

    return {
        "target": "GPU",
        "usage": 0.0,
        "temp": 0.0,
        "vram_used": 0.0,
        "vram_total": 0.0,
    }


def _get_gpu_info_lhm(lhm: object) -> dict | None:
    """Le dados da GPU via LibreHardwareMonitor (NVIDIA e AMD).

    Args:
        lhm: Instancia Computer do LHM.

    Returns:
        dict ou None se falhar.
    """
    try:
        for hw in lhm.Hardware:
            hw_type = str(hw.HardwareType)
            if "Gpu" not in hw_type:
                continue

            hw.Update()
            usage = 0.0
            temp = 0.0
            vram_used = 0.0
            vram_total = 0.0

            for s in hw.Sensors:
                if s.Value is None:
                    continue
                sname = s.Name.lower()
                stype = str(s.SensorType)

                if "core" in sname and stype == "Load":
                    usage = float(s.Value)
                elif "core" in sname and stype == "Temperature":
                    temp = float(s.Value)
                elif "memory total" in sname and stype == "SmallData":
                    vram_total = float(s.Value) / 1024.0
                elif "memory used" in sname and stype == "SmallData":
                    vram_used = float(s.Value) / 1024.0

            return {
                "target": "GPU",
                "usage": round(usage, 1),
                "temp": round(temp, 1),
                "vram_used": round(vram_used, 2),
                "vram_total": round(vram_total, 2),
            }
    except Exception as e:
        logger.debug("Erro LHM GPU: %s", e)
    return None


def _get_gpu_info_pynvml() -> dict | None:
    """Le dados da GPU NVIDIA via pynvml (NVML DLL direta, sem prompt).

    Returns:
        dict ou None se pynvml nao estiver disponivel ou falhar.
    """
    try:
        from pynvml import (
            nvmlInit,
            nvmlShutdown,
            nvmlDeviceGetHandleByIndex,
            nvmlDeviceGetUtilizationRates,
            nvmlDeviceGetTemperature,
            nvmlDeviceGetMemoryInfo,
            NVML_TEMPERATURE_GPU,
        )

        nvmlInit()
        try:
            handle = nvmlDeviceGetHandleByIndex(0)
            util = nvmlDeviceGetUtilizationRates(handle)
            temp = nvmlDeviceGetTemperature(handle, NVML_TEMPERATURE_GPU)
            mem = nvmlDeviceGetMemoryInfo(handle)

            vram_used_gb = mem.used / (1024 * 1024 * 1024)
            vram_total_gb = mem.total / (1024 * 1024 * 1024)

            return {
                "target": "GPU",
                "usage": float(util.gpu),
                "temp": float(temp),
                "vram_used": round(vram_used_gb, 2),
                "vram_total": round(vram_total_gb, 2),
            }
        finally:
            nvmlShutdown()
    except Exception:
        return None


def _get_gpu_info_pyadl() -> dict | None:
    """Le dados da GPU AMD via pyadl (ADL DLL direta, sem prompt).

    Returns:
        dict ou None se pyadl nao estiver disponivel ou falhar.
    """
    try:
        from pyadl import ADLManager

        devices = ADLManager.getDevices()
        if not devices:
            return None

        device = devices[0]
        device.refreshData()

        temp = 0.0
        if hasattr(device, "getTemperature"):
            try:
                temp = float(device.getTemperature())
            except Exception:
                pass

        usage = 0.0
        if hasattr(device, "getCurrentUsage"):
            try:
                usage = float(device.getCurrentUsage())
            except Exception:
                pass

        vram_used = 0.0
        vram_total = 0.0
        if hasattr(device, "getCurrentVRAMUsage") and hasattr(
            device, "getCurrentVRAMSize"
        ):
            try:
                vram_used = float(device.getCurrentVRAMUsage()) / 1024.0
                vram_total = float(device.getCurrentVRAMSize()) / 1024.0
            except Exception:
                pass

        return {
            "target": "GPU",
            "usage": round(usage, 1),
            "temp": round(temp, 1),
            "vram_used": round(vram_used, 2),
            "vram_total": round(vram_total, 2),
        }
    except Exception:
        return None


def shutdown() -> None:
    """Encerra o LHM e libera recursos."""
    global _lhm_computer, _lhm_available, _detected_cpu_vendor, _detected_gpu_vendor
    if _lhm_computer is not None:
        try:
            _lhm_computer.Close()
        except Exception:
            pass
    _lhm_computer = None
    _lhm_available = None
    _detected_cpu_vendor = None
    _detected_gpu_vendor = None
