def fmt_time(secs):
    m, s = divmod(int(secs), 60)

    ms = int((secs % 1) * 10)

    return f"{m:02d}:{s:02d}.{ms}"