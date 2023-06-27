import os
import json

from typing import List, Any
from pathlib import Path

import ipywidgets as widgets
from exif import Image
import pandas as pd


def get_all_paths(path: str, exts: List[str]) -> List[str]:
    all_paths_list = []

    for ext in exts:
        paths = Path(path).glob(f'**/*.{ext}')
        all_paths_list += [str(x) for x in paths if x.is_file()]

    return all_paths_list


def sync_config(imgs_path: str, last_photo_path: str, last_photo_id: str, config_path: str) -> None:
    if not os.path.exists(config_path):
        with open(config_path, 'w') as f:
            f.write('')
            f.close()

    file_content = open(config_path).read()

    if len(file_content) < 5:
        file_content = f'"imgs_path": "{imgs_path}", "last_photo_path": "", "last_photo_id": 0'
        file_content = '{' + file_content + '}'

    config_read = json.loads(file_content)

    if config_read['last_photo_id'] > 0 and last_photo_id == 0:
        return config_read

    config_write = {
        'imgs_path': imgs_path,
        'last_photo_path': last_photo_path,
        'last_photo_id': last_photo_id
    }

    with open(config_path, 'w') as f:
        f.write(json.dumps(config_write))
        f.close()

    return config_read


def main(imgs_path: str, exts: List[str], config_path: str) -> Any:
    global all_paths
    all_paths = get_all_paths(imgs_path, exts)
    all_paths_count = len(all_paths)
    config = sync_config(imgs_path, '', 0, config_path)

    if config['imgs_path'] != imgs_path:
        os.remove(config_path)

    def read_photo() -> None:
        nonlocal current_photo, current_photo_ext
        current_photo_path = all_paths[current_index]
        current_photo = open(current_photo_path, 'rb').read()
        current_ext = os.path.splitext(current_photo_path)[1]

    current_index = config['last_photo_id']
    current_photo = None
    current_photo_ext = ''

    read_photo()

    photo = widgets.Image(
        value=current_photo,
        format=current_photo_ext,
        width=550,
        height=550,
    )

    prev_photo_button = widgets.Button(
        description='Prev photo',
        disabled=False,
        button_style='warning',
        tooltip='Click me',
        icon='check'
    )

    just_save_button = widgets.Button(
        description='Save',
        disabled=False,
        button_style='',
        tooltip='Just save',
        icon='check'
    )

    next_photo_button = widgets.Button(
        description='Next photo',
        disabled=False,
        button_style='success',
        tooltip='Click me',
        icon='check'
    )

    photo_id_label = widgets.Label(f'Photo number: {current_index + 1} / {all_paths_count}')
    photo_path_label = widgets.Label(all_paths[current_index])

    eye_side_btn = widgets.ToggleButtons(
        options=['Left', 'Right'],
        description='Eye side:',
        disabled=False,
        button_style='',
        tooltips=['Left', 'Right'],
    )

    photo_quality_btn = widgets.ToggleButtons(
        options=['Good', 'Acceptable', 'Bad'],
        description='Quality:',
        disabled=False,
        button_style='',
        tooltips=['Left', 'Right'],
    )

    centering_btn = widgets.ToggleButtons(
        options=['Disc', 'Macula', 'No'],
        description='Centering:',
        disabled=False,
        button_style='',
        tooltips=['Disc', 'Macula', 'No'],
    )

    artifacts_btn = widgets.ToggleButtons(
        options=['No', 'Non-obscuring', 'Obscuring'],
        description='Artifacts:',
        disabled=False,
        button_style='',
        tooltips=['No', 'Non-obscuring', 'Obscuring'],
    )

    fov_slider = widgets.IntSlider(
        value=45,
        min=0,
        max=90,
        step=5,
        description='FOV:',
        disabled=False,
        continuous_update=False,
        orientation='horizontal',
        readout=True,
        readout_format='d'
    )

    def update_widgets():
        photo.value = current_photo
        photo.format = current_photo_ext
        photo_id_label.value = f'Current ID: {current_index} / {all_paths_count} (-1)'
        photo_path_label.value = all_paths[current_index]

    def update_config():
        _ = sync_config(imgs_path, all_paths[current_index], current_index, config_path)

    def prev_photo(btn: Any) -> None:
        global current_index
        # save_values()
        current_index -= 1
        read_photo()
        update_widgets()
        update_config()
        read_values()

    def next_photo(btn: Any) -> None:
        global current_index
        save_values()
        current_index += 1
        read_photo()
        update_widgets()
        update_config()
        read_values()

    def just_save(btn: Any) -> None:
        save_values()

    def save_values():
        img = Image(open(all_paths[current_index], 'rb'))
        attrs = {
            'centering': centering_btn.value,
            'artifacts': artifacts_btn.value,
            'fov': fov_slider.value,
            'eye_side': eye_side_btn.value,
            'photo_quality': photo_quality_btn.value
        }
        img.model = json.dumps(attrs)

        with open(all_paths[current_index], 'wb') as f:
            f.write(img.get_file())
            f.close()

    def read_values():
        img = Image(open(all_paths[current_index], 'rb'))
        try:
            attrs = json.loads(img.model)
            centering_btn.value = attrs['centering']
            artifacts_btn.value = attrs['artifacts']
            fov_slider.value = attrs['fov']
            eye_side_btn.value = attrs['eye_side']
            photo_quality_btn.value = attrs['photo_quality']
        except:
            photo_path_label.value += ' (UNLABELLED PHOTO)'
            centering_btn.value = 'Disc'
            artifacts_btn.value = 'No'
            fov_slider.value = 45
            eye_side_btn.value = 'Left'
            photo_quality_btn.value = 'Good'

    read_values()

    prev_photo_button.on_click(prev_photo)
    next_photo_button.on_click(next_photo)
    just_save_button.on_click(just_save)

    photo_col = widgets.VBox([
        photo_id_label, photo_path_label, photo
    ])

    buttons_row = widgets.HBox([
        prev_photo_button, just_save_button, next_photo_button
    ])

    return widgets.VBox([
        photo_col,
        eye_side_btn,
        photo_quality_btn,
        centering_btn,
        artifacts_btn,
        fov_slider,
        buttons_row
    ])


def export_labels(output_path: str) -> None:
    patient_ids = []
    paths = []
    centerings = []
    artifacts = []
    fovs = []
    sides = []
    qualities = []

    for path in all_paths:
        img = Image(open(path, 'rb'))
        attrs = dict()
        try:
            attrs = json.loads(img.model)
            patient_ids.append(Path(path).parent.name)
            paths.append(path)
            centerings.append(attrs['centering'])
            artifacts.append(attrs['artifacts'])
            fovs.append(attrs['fov'])
            sides.append(attrs['eye_side'])
            qualities.append(attrs['photo_quality'])
        except:
            continue

    values_dict = {
        'patient_id': patient_ids,
        'path': paths,
        'centering': centerings,
        'artifacts': artifacts,
        'fov': fovs,
        'eye_side': sides,
        'quality': qualities,
    }

    export_df = pd.DataFrame(values_dict)
    export_df.to_excel(output_path)
