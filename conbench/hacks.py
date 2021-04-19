def get_case(tags):
    case = [
        (k, v)
        for k, v in sorted(tags.items())
        if not isinstance(v, int)
        and v is not None
        and k != "id"
        and k != "name"
        and k != "dataset"
        and k != "source"
        and k != "language"
    ]
    if "language" in tags:
        case.append(("language", tags["language"]))
    return [v for _, v in case]


def set_display_name(benchmark):
    is_api = isinstance(benchmark, dict)
    tags = benchmark["tags"] if is_api else benchmark.case.tags
    name = tags.get("name") if is_api else benchmark.case.name
    if "name" not in tags:
        tags["name"] = name
    case = get_case(tags)
    if "suite" in tags:
        case = [name] + case
    name = ", ".join(case) if case else name
    if is_api:
        benchmark["display_name"] = name
    else:
        benchmark.display_name = name


def set_display_batch(benchmark):
    is_api = isinstance(benchmark, dict)
    tags = benchmark["tags"] if is_api else benchmark.case.tags
    name = tags.get("name") if is_api else benchmark.case.name
    batch = tags.get("suite", name)
    if is_api:
        benchmark["display_batch"] = batch
    else:
        benchmark.display_batch = batch


def sorted_data(benchmarks):
    data = []
    for benchmark in benchmarks:
        tags = benchmark["tags"]
        case = get_case(tags)
        case.append(benchmark["stats"]["mean"])
        data.append(case)

    # Try to sort the cases better
    # unsorted: ['262144/0', '262144/1', '262144/10', '262144/2']
    # sorted: [[262144, 0], [262144, 1], [262144, 2], [262144, 10]]
    new_data = []
    for row in data:
        case = row[0]
        parts = []
        for x in case.split("/"):
            try:
                parts.append(int(x))
            except:
                parts.append(x)
        new_data.append([parts, row])
    new_data = sorted(new_data)

    return [row[1] for row in new_data]
