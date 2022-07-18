import sys
import io
import subprocess
import PIL
import PIL.Image
import re

IM_SIZE = (2048, 2048)
IM_COLOR_BK = (255, 255, 255)


def main():

    im_fr = PIL.Image.open(sys.argv[1])

    if im_fr.size != IM_SIZE:
        return

    im_bk = PIL.Image.new("RGBA", IM_SIZE, IM_COLOR_BK)
    im_bk.copy()

    im = PIL.Image.alpha_composite(im_bk, im_fr)
    im = im.convert("RGB")
    i_buf = io.BytesIO()
    im.save(i_buf, "bmp")

    i_buf.seek(0)

    out = subprocess.run(
        ["bin/potrace", "-b", "svg", "-"],
        input=i_buf.read(),
        capture_output=True,
    )

    v = out.stdout.decode("utf-8").replace(
        "translate(0.000000,2048.000000) scale(0.100000,-0.100000)",
        "translate(-1024.000000,3072.000000) scale(0.1,-0.1)",
    )

    with open(sys.argv[1] + ".svg", "w", encoding="utf-8") as wf:
        wf.write(v)


if __name__ == "__main__":
    main()
