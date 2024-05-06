def get_str_arr_split_by_new_line_from_file(file_path):
    with open(file_path, "r") as file:
        return str(file.read()).split("\n")


def build_request_header(header_item_arr):
    header = {}
    for header_item in header_item_arr:
        if ":" in header_item:
            item_split = header_item.split(":")
            header[item_split[0]] = item_split[1].strip()
    return header
