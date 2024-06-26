import os
import xml.etree.ElementTree as ET
import lmfit
import numpy as np
import matplotlib.pyplot as plt
#
def plot_transmission_spectra_all(ax, root):
    # 그래프에 그릴 데이터를 담을 리스트 초기화
    data_to_plot = []

    WavelengthSweep = list(root.findall('.//WavelengthSweep'))

    # 모든 WavelengthSweep 요소 반복
    for WavelengthSweep in root.findall('.//WavelengthSweep'):
        # DCBias 속성 값 가져오기
        dc_bias = float(WavelengthSweep.get('DCBias'))

        # LengthUnit과 transmission 요소의 text 값 가져오기
        length_values = []
        measured_transmission_values = []
        for L in WavelengthSweep.findall('.//L'):
            length_text = L.text
            length_text = length_text.replace(',', ' ')
            length_values.extend([float(value) for value in length_text.split() if value.strip()])

        for IL in WavelengthSweep.findall('.//IL'):
            measured_transmission_text = IL.text
            measured_transmission_text = measured_transmission_text.replace(',', ' ')
            measured_transmission_values.extend(
                [float(value) for value in measured_transmission_text.split() if value.strip()])

        # 데이터를 데이터 플롯 리스트에 추가
        data_to_plot.append((dc_bias, length_values, measured_transmission_values))

    # 그래프 그리기
    for dc_bias, length_values, measured_transmission_values in data_to_plot:
        ax.plot(length_values, measured_transmission_values, label=f'DCBias={dc_bias}V')

    ax.set_xlabel('Wavelength [nm]')
    ax.set_ylabel('Measured Transmission [dB]')
    ax.set_title(f'Transmission Spectra - as measured')
    ax.legend(title='DC Bias', loc='upper right')
    ax.grid(True)


# 여러 디렉토리 경로
directories = [
    'dat/HY202103/D07/20190715_190855',
    'dat/HY202103/D08/20190526_082853',
    'dat/HY202103/D08/20190528_001012',
    'dat/HY202103/D08/20190712_113254',
    'dat/HY202103/D23/20190528_101900',
    'dat/HY202103/D23/20190531_072042',
    'dat/HY202103/D23/20190603_204847',
    'dat/HY202103/D24/20190528_105459',
    'dat/HY202103/D24/20190528_111731',
    'dat/HY202103/D24/20190531_151815',
    'dat/HY202103/D24/20190603_225101'
]

def find_xml_files(directories):
    device = input("Device (LMZC, LMZO, or all): ").strip().upper()
    wafer_no_input = input("Wafer no (D07, D08, D23, D24, or all): ").strip().upper()
    xml_files = []

    if device not in ['LMZC', 'LMZO', 'all']:
        print("잘못된 device 입력. 'LMZC', 'LMZO', 또는 'all'만 지원됩니다.")
        return []

    if wafer_no_input == 'all':
        wafer_nos = ['D07', 'D08', 'D23', 'D24']
    else:
        wafer_nos = [wafer_no_input]

    for directory in directories:
        try:
            wafer_no = directory.split('/')[2]  # 디렉토리에서 웨이퍼 번호 추출
            if wafer_no in wafer_nos:
                file_list = os.listdir(directory)
                if device == 'LMZC':
                    xml_files.extend([os.path.join(directory, file) for file in file_list if 'LMZC' in file and file.endswith(".xml")])
                elif device == 'LMZO':
                    xml_files.extend([os.path.join(directory, file) for file in file_list if 'LMZO' in file and file.endswith(".xml")])
                elif device == 'ALL':
                    xml_files.extend([os.path.join(directory, file) for file in file_list if ('LMZC' in file or 'LMZO' in file) and file.endswith(".xml")])
        except FileNotFoundError:
            print(f"디렉토리를 찾을 수 없습니다: {directory}")

    return xml_files
