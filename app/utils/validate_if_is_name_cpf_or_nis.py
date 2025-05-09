import re


def validate_if_is_name_cpf_or_nis(input_data: str) -> str:
    cpf_regex = r"\d{3}\.\d{3}\.\d{3}-\d{2}"
    nis_regex = r"\d{1}\.\d{3}\.\d{3}\.\d{3}-\d{1}"
    if re.match(cpf_regex, input_data):
        return "cpf"
    elif re.match(nis_regex, input_data):
        return "nis"
    else:
        return "name"
