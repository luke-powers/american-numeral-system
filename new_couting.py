"""Simple program to output proposed dozenal system.

"""
import argparse
import math

PARSER = argparse.ArgumentParser()
PARSER.add_argument("-n", dest="value", default=723268170687, help="value to convert")
PARSER.add_argument(
    "-p", dest="pronounce", action="store_true", help="spell out name phonetically"
)
PARSER.add_argument("-s", dest="shortcut", action="store_true", help="use shortcuts")
PARSER.add_argument("-t", dest="test", action="store_true", help="run tests")
ARGS = PARSER.parse_args()

SHORTCUTS = {
    "ingom": "nim",  # million
    "inguh": "nuh",  # hundred thousand
    "ingdah": "nah",  # ten thousand
    "ingrhy": "nye",
}  # thousand

BASE = 12
NUMERALS = {
    0: ["x", "zer"],
    1: ["|", "it"],
    2: ["ᗕ", "lee"],
    3: ["ᗒ", "rhy"],
    4: ["ᗐ", "dah"],
    5: ["ᗑ", "uh"],
    6: ["○", "om"],
    7: ["⏀", "we"],
    8: ["ᓀ", "paa"],
    9: ["ᓂ", "fee"],
    10: ["ᑫ", "lo"],
    11: ["ᑯ", "hi"],
}
#        12 is in

TEST_VALUES = {
    723268170687: "hi-inglo-paa-ingfee-lee-ingpaa-ingwe-ingom-om-ingdah-fee-ingrhy-it-fee-rhy",
    143: "hi-hi",  # 99
    144: "inglee",  # 100
    145: "it-zer-it",  # 101
    1727: "hi-hi-hi",
    1728: "ingrhy",
    1729: "ingrhy-zer-zer-it",
    20736: "ingdah",
    3223433: "ingom-hi-ingdah-uh-ingrhy-dah-hi-uh",
    223411: "lo-ingdah-fee-ingrhy-rhy-uh-we",
    223410: "lo-ingdah-fee-ingrhy-rhy-uh-om",
}

if ARGS.test:
    INPUT_RANGE = TEST_VALUES.keys()
    ARGS.pronounce = True
else:
    INPUT_RANGE = ARGS.value if isinstance(ARGS.value, list) else [int(ARGS.value)]
for dec_num in INPUT_RANGE:
    glyph_out = ""
    pro_out = ""
    cur_pow = 12
    rset = None
    tmp_dec_num = dec_num
    while cur_pow >= 1:
        pos_count = rset
        while tmp_dec_num >= int(math.pow(BASE, cur_pow)):
            pos_count = pos_count + 1 if rset != None else 1
            tmp_dec_num -= int(math.pow(BASE, cur_pow))
            rset = 0
        if rset != None:
            glyph, pronunciation = NUMERALS[pos_count]
            glyph_out += glyph
            pro_out += "-" + pronunciation
        cur_pow -= 1
    glyph, pronunciation = NUMERALS[tmp_dec_num]
    glyph_out += glyph
    pro_out += "-" + pronunciation
    print(glyph_out)
    if not ARGS.pronounce:
        break
    split = pro_out.strip("-").split("-")
    pass_1 = ""
    count = len(split) - 1
    for doz_num in split:
        if doz_num is split[-1] and doz_num == "zer":
            pass_1 += "in"
            break
        if count > 2:
            if doz_num != "zer":
                if doz_num != "it":
                    pass_1 += "%s-ing%s-" % (doz_num, NUMERALS[count][-1])
                else:
                    pass_1 += "ing%s-" % (NUMERALS[count][-1])
        else:
            pass_1 += doz_num + "-"
        count -= 1
    output = ""
    if len(split) > 3:
        split2 = pass_1.split("-")
        split2.reverse()
        if split2[:3] == ["in", "zer", "zer"] or split2[:3] == ["zer", "zer", "zer"]:
            while split2[0] == "zer" or split2[0] == "in":
                split2.pop(0)
        split2.reverse()
        pass_2 = "-".join(split2)
        output = pass_2
    else:
        if (pass_1 == "it-zer-zer") or (pass_1 == "it-zer-in"):
            pass_1 = "inglee"
        else:
            last = pass_1.split("-")
            if (
                last[-2] == "zer"
                and (last[-1] == "zer" or last[-1] == "in")
                and not last[-1] is last[-2]
            ):
                pass_1 = last[0] + "-inglee"
        output = pass_1
    output = output.strip("-")
    if ARGS.test:
        if not output == TEST_VALUES[dec_num]:
            print("**failure")
            print(glyph_out)
            print("expected", TEST_VALUES[dec_num])
            print("got     ", output)
            raise Exception("test failed")
    if ARGS.shortcut:
        for phrase in SHORTCUTS:
            if phrase in output:
                output = output.replace(phrase, SHORTCUTS[phrase])
    print(output)
