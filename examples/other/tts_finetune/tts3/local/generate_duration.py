# Copyright (c) 2022 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import argparse
import os
from pathlib import Path

def gen_duration_from_textgrid(inputdir, output, sample_rate=24000,
                               n_shift=300):
    # key: utt_id, value: (speaker, phn_durs)
    durations_dict = {}
    list_dir = os.listdir(inputdir)
    speakers = [dir for dir in list_dir if os.path.isdir(inputdir / dir)]
    for speaker in speakers:
        subdir = inputdir / speaker
        for file in os.listdir(subdir):
            if file.endswith(".TextGrid"):
                tg_path = subdir / file
                name = file.split(".")[0]
                durations_dict[name] = (speaker, readtg(
                    tg_path, sample_rate=sample_rate, n_shift=n_shift))
    with open(output, "w") as wf:
        for name in sorted(durations_dict.keys()):
            wf.write(name + "|" + durations_dict[name][0] + "|" +
                     durations_dict[name][1] + "\n")

if __name__ == '__main__':
    # parse config and args
    parser = argparse.ArgumentParser(
        description="Preprocess audio and then extract features.")

    parser.add_argument(
        "--mfa_dir",
        type=str,
        default="./mfa_result",
        help="directory to save aligned files")

    args = parser.parse_args()

    fs = 24000
    n_shift = 300
    duration_file = "./durations.txt"
    mfa_dir = Path(args.mfa_dir).expanduser()
    mfa_dir.mkdir(parents=True, exist_ok=True)

    gen_duration_from_textgrid(mfa_dir, duration_file, fs, n_shift)


