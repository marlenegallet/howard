import os
import typing
import argparse
import pytest
import json
from os.path import join as osj
from tempfile import TemporaryDirectory
from howard.functions.commons import remove_if_exists
from howard.functions.from_extann import from_extann, read_json
from test_needed import tests_folder


def identical(vcf_list: typing.List[str], begin: str):
    """ """
    vcfs_lines = []
    k = 0
    for vcf in vcf_list:
        vcfs_lines.append([])
        with open(vcf, "r") as f:
            for l in f:
                if not l.startswith(begin):
                    vcfs_lines[k].append(l)
        k += 1
    for i in range(len(vcf_list) - 1):
        assert vcfs_lines[i] == vcfs_lines[i + 1]


def edit_config(configfile, key, new, tmp_dir):
    data = read_json(configfile)
    data[key] = new
    with open(osj(tmp_dir, "param.tmp.json"), "w+") as js:
        json.dump(data, js)
    return osj(tmp_dir, "param.tmp.json")


@pytest.mark.parametrize("mode", ["all", "longest", "chosen"])
def test_from_extann(mode):
    """
    Test from extann func while switching on each mode
    """
    with TemporaryDirectory(dir="/tmp") as tmp_dir:
        input_ex = osj(tests_folder, "databases", "extann", "extann.tsv")
        output_ex = osj(tmp_dir, f"OMIM.output.{mode}.bed")
        param = osj(tests_folder, "data", "example.param.extann.json")
        param_ex = edit_config(param, "mode_extann", mode, tmp_dir)
        expected_ex = osj(
            tests_folder, "databases", "extann", f"extann.expected.{mode}.bed"
        )

        # remove
        remove_if_exists([output_ex])
        remove_if_exists([output_ex + ".hdr"])

        args = argparse.Namespace(
            input_extann=input_ex,
            output_extann=output_ex,
            param_extann=param_ex,
            refgene=osj(
                tests_folder,
                "databases",
                "extann",
                "ncbiRefSeq.chunk.bed.gz",
            ),
            transcripts=osj(tests_folder, "data", "transcripts.from_extann.tsv"),
            mode_extann=mode,
        )
        from_extann(args)

        assert os.path.exists(output_ex)
        assert os.path.exists(output_ex + ".hdr")
        identical([expected_ex, output_ex], "##")
