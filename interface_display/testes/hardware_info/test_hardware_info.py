import psutil
from unittest.mock import MagicMock, patch

import pytest

from modules.hardware_info import detect_cpu_vendor, detect_gpu_vendor, detect_hardware
from modules.hardware_info import get_cpu_info, get_gpu_info
from modules.hardware_info import shutdown as hw_shutdown
from modules.hardware_info import _get_cpu_info_wmi


def _reset_vendor_state():
    """Reseta o estado global de vendors detectados entre testes."""
    import modules.hardware_info as mod
    mod._detected_cpu_vendor = None
    mod._detected_gpu_vendor = None


def _make_sensor(name, stype, value):
    """Cria um mock de sensor LHM com nome, tipo e valor."""
    s = MagicMock()
    s.Name = name
    s.SensorType = stype
    s.Value = value
    return s


class TestGetCpuInfoLhm:
    """Testes para CPU via LibreHardwareMonitor."""

    def test_lhm_returns_correct_format(self):
        """Caminho Feliz: LHM retorna dados CPU validos."""
        sensors = [
            _make_sensor("CPU Total", "Load", 55.5),
            _make_sensor("Core (Tctl/Tdie)", "Temperature", 65.0),
            _make_sensor("Cores (Average)", "Clock", 3600.0),
        ]

        mock_hw = MagicMock()
        mock_hw.HardwareType = "Cpu"
        mock_hw.Name = "Intel Core i7-10700K"
        mock_hw.Sensors = sensors

        mock_lhm = MagicMock()
        mock_lhm.Hardware = [mock_hw]

        mock_lhm_mod = MagicMock()
        mock_lhm_mod.Hardware.HardwareType = MagicMock()

        with patch.dict(
            "sys.modules",
            {
                "LibreHardwareMonitor": mock_lhm_mod,
                "LibreHardwareMonitor.Hardware": mock_lhm_mod.Hardware,
            },
        ):
            from modules.hardware_info import _get_cpu_info_lhm
            result = _get_cpu_info_lhm(mock_lhm)

        assert result is not None
        assert result["target"] == "CPU"
        assert result["usage"] == 55.5
        assert result["temp"] == 65.0
        assert result["clock"] == 3600

    def test_lhm_no_cpu_hardware_returns_none(self):
        """Falha: LHM sem hardware CPU, retorna None."""
        mock_lhm = MagicMock()
        mock_lhm.Hardware = []

        from modules.hardware_info import _get_cpu_info_lhm

        result = _get_cpu_info_lhm(mock_lhm)

        assert result is None

    def test_lhm_exception_returns_none(self):
        """Falha: LHM lanca excecao, retorna None."""
        mock_lhm = MagicMock()
        mock_hw = MagicMock()
        mock_hw.HardwareType.__str__ = lambda s: "Cpu"
        mock_hw.Update.side_effect = Exception("crash")
        mock_lhm.Hardware = [mock_hw]

        from modules.hardware_info import _get_cpu_info_lhm

        result = _get_cpu_info_lhm(mock_lhm)

        assert result is None


class TestGetCpuInfoPsutilFallback:
    """Testes para CPU via psutil (fallback com LHM desabilitado)."""

    def teardown_method(self):
        """Reseta estado global de vendors apos cada teste."""
        _reset_vendor_state()

    @patch("modules.hardware_info._get_cpu_info_wmi", return_value=None)
    @patch("modules.hardware_info._get_lhm", return_value=None)
    @patch("modules.hardware_info.psutil")
    @patch("modules.hardware_info.platform")
    def test_returns_correct_format(self, mock_platform, mock_psutil, mock_lhm, mock_wmi):
        """Caminho Feliz: psutil retorna dict com chaves corretas."""
        mock_platform.system.return_value = "Linux"
        mock_platform.processor.return_value = "Intel(R) Core(TM) i7"
        mock_psutil.cpu_percent.return_value = 55.5
        mock_freq = MagicMock()
        mock_freq.current = 3600
        mock_psutil.cpu_freq.return_value = mock_freq
        mock_psutil.sensors_temperatures.return_value = {
            "coretemp": [MagicMock(current=65.0)]
        }

        result = get_cpu_info()

        assert result["target"] == "CPU"
        assert result["usage"] == 55.5
        assert result["temp"] == 65.0

    @patch("modules.hardware_info._get_cpu_info_wmi", return_value=None)
    @patch("modules.hardware_info._get_lhm", return_value=None)
    @patch("modules.hardware_info.psutil")
    @patch("modules.hardware_info.platform")
    def test_no_freq_returns_zero_clock(self, mock_platform, mock_psutil, mock_lhm, mock_wmi):
        """Falha: cpu_freq None, clock deve ser 0."""
        mock_platform.processor.return_value = "Intel(R) Core(TM)"
        mock_psutil.cpu_percent.return_value = 30.0
        mock_psutil.cpu_freq.return_value = None

        result = get_cpu_info()

        assert result["clock"] == 0


class TestGetCpuInfoRealPsutil:
    """Testes de integracao com psutil real."""

    def test_works_with_real_psutil(self):
        """Integracao: get_cpu_info funciona sem crash no ambiente real."""
        result = get_cpu_info()

        assert result["target"] == "CPU"
        assert isinstance(result["usage"], float)
        assert isinstance(result["temp"], float)
        assert isinstance(result["clock"], int)
        assert 0.0 <= result["usage"] <= 100.0


class TestGetCpuInfoRealIntegration:
    """Teste de integracao: verifica clock > 0 no Windows real (WMI fallback)."""

    def test_clock_greater_than_zero(self):
        """Integracao: clock deve ser > 0 (WMI ou LHM fornece clock real)."""
        _reset_vendor_state()
        try:
            result = get_cpu_info()
            assert result["clock"] > 0, f"clock={result['clock']}, esperado > 0"
        finally:
            hw_shutdown()


class TestGetCpuInfoWmi:
    """Testes para CPU via WMI (Win32_Processor)."""

    def teardown_method(self):
        """Reseta estado global de vendors apos cada teste."""
        _reset_vendor_state()

    def test_wmi_returns_correct_format(self):
        """Caminho Feliz: WMI retorna dados CPU validos."""
        mock_cpu = MagicMock()
        mock_cpu.LoadPercentage = 42
        mock_cpu.CurrentClockSpeed = 3600

        mock_wmi_instance = MagicMock()
        mock_wmi_instance.Win32_Processor.return_value = [mock_cpu]

        mock_wmi_mod = MagicMock()
        mock_wmi_mod.WMI.return_value = mock_wmi_instance

        with patch.dict("sys.modules", {"wmi": mock_wmi_mod}):
            result = _get_cpu_info_wmi()

        assert result is not None
        assert result["target"] == "CPU"
        assert result["usage"] == 42.0
        assert result["clock"] == 3600
        assert result["temp"] == 0.0

    def test_wmi_no_processor_returns_none(self):
        """Falha: WMI sem processador, retorna None."""
        mock_wmi_instance = MagicMock()
        mock_wmi_instance.Win32_Processor.return_value = []

        mock_wmi_mod = MagicMock()
        mock_wmi_mod.WMI.return_value = mock_wmi_instance

        with patch.dict("sys.modules", {"wmi": mock_wmi_mod}):
            result = _get_cpu_info_wmi()

        assert result is None

    def test_wmi_exception_returns_none(self):
        """Falha: WMI lanca excecao, retorna None."""
        mock_wmi_mod = MagicMock()
        mock_wmi_mod.WMI.side_effect = Exception("WMI unavailable")

        with patch.dict("sys.modules", {"wmi": mock_wmi_mod}):
            result = _get_cpu_info_wmi()

        assert result is None

    def test_wmi_null_fields_uses_zero(self):
        """Falha: Campos None do WMI viram 0."""
        mock_cpu = MagicMock()
        mock_cpu.LoadPercentage = None
        mock_cpu.CurrentClockSpeed = None

        mock_wmi_instance = MagicMock()
        mock_wmi_instance.Win32_Processor.return_value = [mock_cpu]

        mock_wmi_mod = MagicMock()
        mock_wmi_mod.WMI.return_value = mock_wmi_instance

        with patch.dict("sys.modules", {"wmi": mock_wmi_mod}):
            result = _get_cpu_info_wmi()

        assert result is not None
        assert result["usage"] == 0.0
        assert result["clock"] == 0


class TestLhmZeroFallthrough:
    """Testes: LHM CPU com temp=0 e clock=0 retorna None (fallthrough)."""

    def test_lhm_zero_temp_zero_clock_returns_none(self):
        """LHM retorna None quando temp e clock estao zerados."""
        sensors = [
            _make_sensor("CPU Total", "Load", 55.5),
            _make_sensor("Core (Tctl/Tdie)", "Temperature", 0.0),
            _make_sensor("Cores (Average)", "Clock", 0.0),
        ]

        mock_hw = MagicMock()
        mock_hw.HardwareType = "Cpu"
        mock_hw.Sensors = sensors

        mock_lhm = MagicMock()
        mock_lhm.Hardware = [mock_hw]

        mock_lhm_mod = MagicMock()

        with patch.dict(
            "sys.modules",
            {
                "LibreHardwareMonitor": mock_lhm_mod,
                "LibreHardwareMonitor.Hardware": mock_lhm_mod.Hardware,
            },
        ):
            from modules.hardware_info import _get_cpu_info_lhm
            result = _get_cpu_info_lhm(mock_lhm)

        assert result is None

    def test_lhm_zero_temp_nonzero_clock_returns_dict(self):
        """LHM retorna dict quando clock > 0 mesmo com temp=0."""
        sensors = [
            _make_sensor("CPU Total", "Load", 55.5),
            _make_sensor("Core (Tctl/Tdie)", "Temperature", 0.0),
            _make_sensor("Cores (Average)", "Clock", 3600.0),
        ]

        mock_hw = MagicMock()
        mock_hw.HardwareType = "Cpu"
        mock_hw.Sensors = sensors

        mock_lhm = MagicMock()
        mock_lhm.Hardware = [mock_hw]

        mock_lhm_mod = MagicMock()

        with patch.dict(
            "sys.modules",
            {
                "LibreHardwareMonitor": mock_lhm_mod,
                "LibreHardwareMonitor.Hardware": mock_lhm_mod.Hardware,
            },
        ):
            from modules.hardware_info import _get_cpu_info_lhm
            result = _get_cpu_info_lhm(mock_lhm)

        assert result is not None
        assert result["clock"] == 3600

    def test_lhm_nonzero_temp_zero_clock_returns_dict(self):
        """LHM retorna dict quando temp > 0 mesmo com clock=0."""
        sensors = [
            _make_sensor("CPU Total", "Load", 55.5),
            _make_sensor("Core (Tctl/Tdie)", "Temperature", 65.0),
            _make_sensor("Cores (Average)", "Clock", 0.0),
        ]

        mock_hw = MagicMock()
        mock_hw.HardwareType = "Cpu"
        mock_hw.Sensors = sensors

        mock_lhm = MagicMock()
        mock_lhm.Hardware = [mock_hw]

        mock_lhm_mod = MagicMock()

        with patch.dict(
            "sys.modules",
            {
                "LibreHardwareMonitor": mock_lhm_mod,
                "LibreHardwareMonitor.Hardware": mock_lhm_mod.Hardware,
            },
        ):
            from modules.hardware_info import _get_cpu_info_lhm
            result = _get_cpu_info_lhm(mock_lhm)

        assert result is not None
        assert result["temp"] == 65.0


class TestCpuFallbackChain:
    """Testes para a cadeia de fallback CPU: LHM -> WMI -> psutil."""

    def teardown_method(self):
        """Reseta estado global de vendors apos cada teste."""
        _reset_vendor_state()

    @patch("modules.hardware_info.detect_cpu_vendor", return_value="AMD")
    @patch("modules.hardware_info._get_cpu_info_psutil")
    @patch("modules.hardware_info._get_cpu_info_wmi")
    @patch("modules.hardware_info._get_lhm")
    def test_lhm_fails_wmi_succeeds(self, mock_lhm, mock_wmi, mock_psutil, mock_vendor):
        """LHM retorna None (zerado), WMI retorna dados."""
        mock_lhm.return_value = MagicMock()
        mock_lhm_instance = mock_lhm.return_value

        mock_hw = MagicMock()
        mock_hw.HardwareType = "Cpu"
        mock_hw.Sensors = [
            _make_sensor("Core (Tctl/Tdie)", "Temperature", 0.0),
            _make_sensor("Cores (Average)", "Clock", 0.0),
        ]
        mock_lhm_instance.Hardware = [mock_hw]
        mock_lhm_instance.HardwareType = MagicMock()

        mock_wmi.return_value = {
            "target": "CPU",
            "usage": 42.0,
            "temp": 0.0,
            "clock": 3600,
        }

        result = get_cpu_info()

        assert result["clock"] == 3600
        assert result["usage"] == 42.0
        mock_psutil.assert_not_called()

    @patch("modules.hardware_info.detect_cpu_vendor", return_value="AMD")
    @patch("modules.hardware_info._get_cpu_info_psutil")
    @patch("modules.hardware_info._get_cpu_info_wmi", return_value=None)
    @patch("modules.hardware_info._get_lhm", return_value=None)
    def test_lhm_wmi_fail_psutil_succeeds(self, mock_lhm, mock_wmi, mock_psutil, mock_vendor):
        """LHM e WMI falham, psutil retorna dados."""
        mock_psutil.return_value = {
            "target": "CPU",
            "usage": 30.0,
            "temp": 0.0,
            "clock": 3001,
        }

        result = get_cpu_info()

        assert result["clock"] == 3001


class TestGetGpuInfoLhm:
    """Testes para GPU via LibreHardwareMonitor."""

    def test_lhm_nvidia_returns_correct_format(self):
        """Caminho Feliz: LHM retorna dados GPU NVIDIA validos."""
        sensors = [
            _make_sensor("GPU Core", "Load", 80.0),
            _make_sensor("GPU Core", "Temperature", 71.0),
            _make_sensor("GPU Memory Total", "SmallData", 8192.0),
            _make_sensor("GPU Memory Used", "SmallData", 2048.0),
        ]

        mock_hw = MagicMock()
        mock_hw.HardwareType.__str__ = lambda s: "GpuNvidia"
        mock_hw.Sensors = sensors

        mock_lhm = MagicMock()
        mock_lhm.Hardware = [mock_hw]

        from modules.hardware_info import _get_gpu_info_lhm

        result = _get_gpu_info_lhm(mock_lhm)

        assert result is not None
        assert result["target"] == "GPU"
        assert result["usage"] == 80.0
        assert result["temp"] == 71.0
        assert result["vram_total"] == 8.0
        assert result["vram_used"] == 2.0

    def test_lhm_amd_gpu(self):
        """Caminho Feliz: LHM detecta GPU AMD."""
        sensors = [
            _make_sensor("GPU Core", "Load", 45.0),
            _make_sensor("GPU Core", "Temperature", 55.0),
            _make_sensor("GPU Memory Total", "SmallData", 12288.0),
            _make_sensor("GPU Memory Used", "SmallData", 4096.0),
        ]

        mock_hw = MagicMock()
        mock_hw.HardwareType.__str__ = lambda s: "GpuAmd"
        mock_hw.Sensors = sensors

        mock_lhm = MagicMock()
        mock_lhm.Hardware = [mock_hw]

        from modules.hardware_info import _get_gpu_info_lhm

        result = _get_gpu_info_lhm(mock_lhm)

        assert result is not None
        assert result["target"] == "GPU"
        assert result["usage"] == 45.0
        assert result["vram_total"] == 12.0

    def test_lhm_no_gpu_returns_none(self):
        """Falha: LHM sem GPU, retorna None."""
        mock_lhm = MagicMock()
        mock_lhm.Hardware = []

        from modules.hardware_info import _get_gpu_info_lhm

        result = _get_gpu_info_lhm(mock_lhm)

        assert result is None


class TestGetGpuInfoPynvml:
    """Testes para GPU NVIDIA via pynvml."""

    def teardown_method(self):
        """Reseta estado global de vendors apos cada teste."""
        _reset_vendor_state()

    @patch("modules.hardware_info.detect_gpu_vendor", return_value="NVIDIA")
    @patch("modules.hardware_info._get_gpu_info_pyadl", return_value=None)
    @patch("modules.hardware_info._get_gpu_info_pynvml")
    @patch("modules.hardware_info._get_lhm", return_value=None)
    def test_pynvml_returns_correct_format(
        self, mock_lhm, mock_pynvml, mock_pyadl, mock_gpu_vendor
    ):
        """Caminho Feliz: pynvml retorna dados validos (LHM desabilitado)."""
        mock_pynvml.return_value = {
            "target": "GPU",
            "usage": 80.0,
            "temp": 71.0,
            "vram_used": 2.0,
            "vram_total": 8.0,
        }

        result = get_gpu_info()

        assert result["usage"] == 80.0

    def test_pynvml_not_available_returns_none(self):
        """Falha: pynvml indisponivel (sem NVIDIA), retorna None."""
        mock_pynvml = MagicMock()
        mock_pynvml.nvmlInit.side_effect = Exception("NVML not found")
        with patch.dict("sys.modules", {"pynvml": mock_pynvml}):
            from modules.hardware_info import _get_gpu_info_pynvml
            result = _get_gpu_info_pynvml()

        assert result is None


class TestGetGpuInfoPyadl:
    """Testes para GPU AMD via pyadl."""

    def teardown_method(self):
        """Reseta estado global de vendors apos cada teste."""
        _reset_vendor_state()

    @patch("modules.hardware_info.detect_gpu_vendor", return_value="AMD")
    @patch("modules.hardware_info._get_gpu_info_pyadl")
    @patch("modules.hardware_info._get_gpu_info_pynvml", return_value=None)
    @patch("modules.hardware_info._get_lhm", return_value=None)
    def test_pyadl_returns_correct_format(
        self, mock_lhm, mock_pynvml, mock_pyadl, mock_gpu_vendor
    ):
        """Caminho Feliz: pyadl retorna dados AMD validos (LHM desabilitado)."""
        mock_pyadl.return_value = {
            "target": "GPU",
            "usage": 50.0,
            "temp": 60.0,
            "vram_used": 4.0,
            "vram_total": 12.0,
        }

        result = get_gpu_info()

        assert result["usage"] == 50.0
        assert result["vram_total"] == 12.0

    def test_pyadl_no_amd_returns_none(self):
        """Falha: pyadl sem GPU AMD, retorna None."""
        mock_pyadl = MagicMock()
        mock_pyadl.ADLManager.getDevices.return_value = []
        with patch.dict("sys.modules", {"pyadl": mock_pyadl}):
            from modules.hardware_info import _get_gpu_info_pyadl
            result = _get_gpu_info_pyadl()

        assert result is None


class TestGetGpuInfoFullFallback:
    """Teste da cadeia completa de fallbacks."""

    def teardown_method(self):
        """Reseta estado global de vendors apos cada teste."""
        _reset_vendor_state()

    @patch("modules.hardware_info.detect_gpu_vendor", return_value="Unknown")
    @patch("modules.hardware_info._get_gpu_info_pyadl", return_value=None)
    @patch("modules.hardware_info._get_gpu_info_pynvml", return_value=None)
    @patch("modules.hardware_info._get_lhm", return_value=None)
    def test_all_fail_returns_zeros(self, mock_lhm, mock_nvml, mock_adl, mock_vendor):
        """Falha: Todos os backends falham, retorna zeros."""
        result = get_gpu_info()

        assert result["target"] == "GPU"
        assert result["usage"] == 0.0
        assert result["temp"] == 0.0
        assert result["vram_used"] == 0.0
        assert result["vram_total"] == 0.0


class TestShutdown:
    """Testes para a funcao shutdown."""

    def test_shutdown_when_no_lhm(self):
        """Caminho Feliz: shutdown sem LHM ativo nao crasha."""
        from modules.hardware_info import shutdown, _lhm_computer

        shutdown()


class TestDetectCpuVendor:
    """Testes para detect_cpu_vendor."""

    def teardown_method(self):
        """Reseta estado global de vendors apos cada teste."""
        _reset_vendor_state()

    @patch("modules.hardware_info._get_lhm", return_value=None)
    @patch("modules.hardware_info.platform")
    def test_detects_intel_via_platform(self, mock_platform, mock_lhm):
        """Caminho Feliz: Detecta Intel via platform.processor()."""
        mock_platform.processor.return_value = "Intel(R) Core(TM) i7-10700K"

        result = detect_cpu_vendor()

        assert result == "Intel"

    @patch("modules.hardware_info._get_lhm", return_value=None)
    @patch("modules.hardware_info.platform")
    def test_detects_amd_via_platform(self, mock_platform, mock_lhm):
        """Caminho Feliz: Detecta AMD via platform.processor()."""
        mock_platform.processor.return_value = "AMD Ryzen 7 5800X"

        result = detect_cpu_vendor()

        assert result == "AMD"

    @patch("modules.hardware_info._get_lhm", return_value=None)
    @patch("modules.hardware_info.platform")
    def test_unknown_vendor_via_platform(self, mock_platform, mock_lhm):
        """Falha: String nao reconhecida retorna Unknown."""
        mock_platform.processor.return_value = "GenericCPU v1"

        result = detect_cpu_vendor()

        assert result == "Unknown"

    def test_detects_intel_via_lhm(self):
        """Caminho Feliz: Detecta Intel via LHM hardware name."""
        mock_hw = MagicMock()
        mock_hw.HardwareType = "Cpu"
        mock_hw.Name = "Intel Core i7-10700K"

        mock_lhm = MagicMock()
        mock_lhm.Hardware = [mock_hw]

        with patch("modules.hardware_info._get_lhm", return_value=mock_lhm):
            result = detect_cpu_vendor()

        assert result == "Intel"

    def test_detects_amd_via_lhm(self):
        """Caminho Feliz: Detecta AMD via LHM hardware name."""
        mock_hw = MagicMock()
        mock_hw.HardwareType = "Cpu"
        mock_hw.Name = "AMD Ryzen 9 5900X"

        mock_lhm = MagicMock()
        mock_lhm.Hardware = [mock_hw]

        with patch("modules.hardware_info._get_lhm", return_value=mock_lhm):
            result = detect_cpu_vendor()

        assert result == "AMD"

    def test_caches_result(self):
        """Caminho Feliz: Segunda chamada retorna valor em cache."""
        import modules.hardware_info as mod
        mod._detected_cpu_vendor = "Intel"

        result = detect_cpu_vendor()

        assert result == "Intel"


class TestDetectGpuVendor:
    """Testes para detect_gpu_vendor."""

    def teardown_method(self):
        """Reseta estado global de vendors apos cada teste."""
        _reset_vendor_state()

    def test_detects_nvidia_via_lhm(self):
        """Caminho Feliz: Detecta NVIDIA via LHM HardwareType."""
        mock_hw = MagicMock()
        mock_hw.HardwareType.__str__ = lambda s: "GpuNvidia"

        mock_lhm = MagicMock()
        mock_lhm.Hardware = [mock_hw]

        with patch("modules.hardware_info._get_lhm", return_value=mock_lhm):
            result = detect_gpu_vendor()

        assert result == "NVIDIA"

    def test_detects_amd_via_lhm(self):
        """Caminho Feliz: Detecta AMD via LHM HardwareType."""
        mock_hw = MagicMock()
        mock_hw.HardwareType.__str__ = lambda s: "GpuAmd"

        mock_lhm = MagicMock()
        mock_lhm.Hardware = [mock_hw]

        with patch("modules.hardware_info._get_lhm", return_value=mock_lhm):
            result = detect_gpu_vendor()

        assert result == "AMD"

    def test_detects_intel_via_lhm(self):
        """Caminho Feliz: Detecta Intel via LHM HardwareType."""
        mock_hw = MagicMock()
        mock_hw.HardwareType.__str__ = lambda s: "GpuIntel"

        mock_lhm = MagicMock()
        mock_lhm.Hardware = [mock_hw]

        with patch("modules.hardware_info._get_lhm", return_value=mock_lhm):
            result = detect_gpu_vendor()

        assert result == "Intel"

    @patch("modules.hardware_info._get_lhm", return_value=None)
    def test_fallback_wmi_nvidia(self, mock_lhm):
        """Caminho Feliz: Detecta NVIDIA via WMI fallback."""
        mock_gpu = MagicMock()
        mock_gpu.Name = "NVIDIA GeForce RTX 3080"

        mock_wmi_instance = MagicMock()
        mock_wmi_instance.Win32_VideoController.return_value = [mock_gpu]

        mock_wmi_mod = MagicMock()
        mock_wmi_mod.WMI.return_value = mock_wmi_instance

        with patch.dict("sys.modules", {"wmi": mock_wmi_mod}):
            result = detect_gpu_vendor()

        assert result == "NVIDIA"

    @patch("modules.hardware_info._get_lhm", return_value=None)
    def test_fallback_wmi_amd(self, mock_lhm):
        """Caminho Feliz: Detecta AMD via WMI fallback."""
        mock_gpu = MagicMock()
        mock_gpu.Name = "AMD Radeon RX 6800 XT"

        mock_wmi_instance = MagicMock()
        mock_wmi_instance.Win32_VideoController.return_value = [mock_gpu]

        mock_wmi_mod = MagicMock()
        mock_wmi_mod.WMI.return_value = mock_wmi_instance

        with patch.dict("sys.modules", {"wmi": mock_wmi_mod}):
            result = detect_gpu_vendor()

        assert result == "AMD"

    @patch("modules.hardware_info._get_lhm", return_value=None)
    def test_fallback_wmi_intel(self, mock_lhm):
        """Caminho Feliz: Detecta Intel via WMI fallback."""
        mock_gpu = MagicMock()
        mock_gpu.Name = "Intel(R) UHD Graphics 630"

        mock_wmi_instance = MagicMock()
        mock_wmi_instance.Win32_VideoController.return_value = [mock_gpu]

        mock_wmi_mod = MagicMock()
        mock_wmi_mod.WMI.return_value = mock_wmi_instance

        with patch.dict("sys.modules", {"wmi": mock_wmi_mod}):
            result = detect_gpu_vendor()

        assert result == "Intel"

    @patch("modules.hardware_info._get_lhm", return_value=None)
    def test_wmi_unavailable_returns_unknown(self, mock_lhm):
        """Falha: WMI indisponivel retorna Unknown."""
        with patch.dict("sys.modules", {"wmi": None}):
            result = detect_gpu_vendor()

        assert result == "Unknown"

    @patch("modules.hardware_info._get_lhm")
    def test_lhm_no_gpu_returns_unknown(self, mock_lhm):
        """Falha: LHM sem GPU retorna Unknown via fallback."""
        mock_lhm_instance = MagicMock()
        mock_lhm_instance.Hardware = []
        mock_lhm.return_value = mock_lhm_instance

        with patch.dict("sys.modules", {"wmi": None}):
            result = detect_gpu_vendor()

        assert result == "Unknown"

    def test_caches_result(self):
        """Caminho Feliz: Segunda chamada retorna valor em cache."""
        import modules.hardware_info as mod
        mod._detected_gpu_vendor = "AMD"

        result = detect_gpu_vendor()

        assert result == "AMD"


class TestDetectHardware:
    """Testes para detect_hardware."""

    def teardown_method(self):
        """Reseta estado global de vendors apos cada teste."""
        _reset_vendor_state()

    @patch("modules.hardware_info.detect_gpu_vendor", return_value="NVIDIA")
    @patch("modules.hardware_info.detect_cpu_vendor", return_value="Intel")
    def test_returns_full_info(self, mock_cpu, mock_gpu):
        """Caminho Feliz: Retorna dict com vendors e libs."""
        result = detect_hardware()

        assert result["cpu_vendor"] == "Intel"
        assert result["gpu_vendor"] == "NVIDIA"
        assert result["cpu_libs"] == ["lhm", "wmi", "psutil"]
        assert result["gpu_libs"] == ["lhm", "pynvml"]

    @patch("modules.hardware_info.detect_gpu_vendor", return_value="AMD")
    @patch("modules.hardware_info.detect_cpu_vendor", return_value="AMD")
    def test_amd_setup(self, mock_cpu, mock_gpu):
        """Caminho Feliz: Setup AMD usa pyadl."""
        result = detect_hardware()

        assert result["gpu_libs"] == ["lhm", "pyadl"]

    @patch("modules.hardware_info.detect_gpu_vendor", return_value="Intel")
    @patch("modules.hardware_info.detect_cpu_vendor", return_value="Intel")
    def test_intel_gpu_only_lhm(self, mock_cpu, mock_gpu):
        """Caminho Feliz: Intel GPU so usa LHM."""
        result = detect_hardware()

        assert result["gpu_libs"] == ["lhm"]
