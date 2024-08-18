from __future__ import annotations

from typing import TYPE_CHECKING

from randovania.games.samus_returns.gui.generated.preset_msr_chaos_ui import Ui_PresetMSRChaos
from randovania.games.samus_returns.layout.msr_configuration import MSRConfiguration
from randovania.gui.preset_settings.preset_tab import PresetTab

if TYPE_CHECKING:
    from randovania.game_description.game_description import GameDescription
    from randovania.gui.lib.window_manager import WindowManager
    from randovania.interface_common.preset_editor import PresetEditor
    from randovania.layout.preset import Preset


class PresetMSRChaos(PresetTab, Ui_PresetMSRChaos):
    def __init__(self, editor: PresetEditor, game_description: GameDescription, window_manager: WindowManager) -> None:
        super().__init__(editor, game_description, window_manager)

        self.setupUi(self)
        self.superheated_slider.valueChanged.connect(self._on_slider_changed)
        self.submerged_lava_slider.valueChanged.connect(self._on_slider_changed)
        self.submerged_water_slider.valueChanged.connect(self._on_slider_changed)
        self.submerged_acid_slider.valueChanged.connect(self._on_slider_changed)

        self._change_sliders()

    def _on_slider_changed(self):
        self._change_sliders()
        self._update_editor()

    def _change_sliders(self) -> None:
        self.superheated_slider.setMaximum(
            1000
            - self.submerged_lava_slider.value()
            - self.submerged_water_slider.value()
            - self.submerged_acid_slider.value()
        )
        self.superheated_slider.setEnabled(self.superheated_slider.maximum() > 0)
        self.submerged_lava_slider.setMaximum(
            1000
            - self.superheated_slider.value()
            - self.submerged_water_slider.value()
            - self.submerged_acid_slider.value()
        )
        self.submerged_lava_slider.setEnabled(self.submerged_lava_slider.maximum() > 0)
        self.submerged_water_slider.setMaximum(
            1000
            - self.superheated_slider.value()
            - self.submerged_lava_slider.value()
            - self.submerged_acid_slider.value()
        )
        self.submerged_water_slider.setEnabled(self.submerged_water_slider.maximum() > 0)
        self.submerged_acid_slider.setMaximum(
            1000
            - self.superheated_slider.value()
            - self.submerged_lava_slider.value()
            - self.submerged_water_slider.value()
        )
        self.submerged_acid_slider.setEnabled(self.submerged_acid_slider.maximum() > 0)

        self.superheated_slider_label.setText(f"{self.superheated_slider.value() / 10.0:.1f}%")
        self.submerged_lava_slider_label.setText(f"{self.submerged_lava_slider.value() / 10.0:.1f}%")
        self.submerged_water_slider_label.setText(f"{self.submerged_water_slider.value() / 10.0:.1f}%")
        self.submerged_acid_slider_label.setText(f"{self.submerged_acid_slider.value() / 10.0:.1f}%")

    @classmethod
    def tab_title(cls) -> str:
        return "Chaos Settings"

    @classmethod
    def uses_patches_tab(cls) -> bool:
        return True

    def on_preset_changed(self, preset: Preset) -> None:
        assert isinstance(preset.configuration, MSRConfiguration)
        self.superheated_slider.setValue(preset.configuration.superheated_probability)
        self.submerged_lava_slider.setValue(preset.configuration.submerged_lava_probability)
        self.submerged_water_slider.setValue(preset.configuration.submerged_water_probability)
        self.submerged_acid_slider.setValue(preset.configuration.submerged_acid_probability)

    def _update_editor(self) -> None:
        with self._editor as editor:
            editor.set_configuration_field("superheated_probability", self.superheated_slider.value())
            editor.set_configuration_field("submerged_lava_probability", self.submerged_lava_slider.value())
            editor.set_configuration_field("submerged_water_probability", self.submerged_water_slider.value())
            editor.set_configuration_field("submerged_acid_probability", self.submerged_acid_slider.value())
