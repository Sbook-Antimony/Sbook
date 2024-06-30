def quote(txt):
    fl, *lns = txt.splitlines()
    ret = "> " + fl
    for ln in lns:
        ret += "\n  " + ln
    return ret
