from log_file_content import LOG_FILE_CONTENT


def extract_domain(domain: str) -> str:
    """
    Extracts the domain to the required levels (2 or 3 levels based on specific rules).

    Args:
        domain (str): The original domain from the log file.

    Returns:
        str: The formatted domain.
    """
    domain_parts = domain.strip("*").split(".")
    if len(domain_parts) > 2 and (
        domain_parts[-2] == "co" or domain_parts[-2] == "com"
    ):
        return ".".join(domain_parts[-3:])
    else:
        return ".".join(domain_parts[-2:])



def aggregate_counts(log_file: str) -> dict:
    """
    Aggregates access counts for each formatted domain from the log file.

    Args:
        log_file (str): Multi-line string with domain names and their associated numbers.

    Returns:
        dict: Dictionary with formatted domain names as keys and their aggregated counts as values.
    """
    domains_count = {}
    lines = log_file.strip().split("\n")
    for line in lines:
        parts = line.split()
        domain, count = parts
        count = int(count)
        formatted_domain = extract_domain(domain)
        if formatted_domain in domains_count:
            domains_count[formatted_domain] += count
        else:
            domains_count[formatted_domain] = count
    return domains_count

def formatted_output(domains_count: dict, min_hits: int) -> str:
    """
    Formats the output by sorting and filtering domains based on the minimum hit count.

    Args:
        domains_count (dict): Dictionary with domain names and their associated counts.
        min_hits (int): Minimum hit count to include a domain in the output.

    Returns:
        str: Formatted string with domains and their counts.
    """
    sorted_domains = sorted(domains_count.items(), key=lambda item: (-item[1], item[0]))

    output_lines = [
        f"{domain},({count})" for domain, count in sorted_domains if count >= min_hits
    ]
    return "\n".join(output_lines)


def count_domains(log_file: str, min_hits: int) -> str:
    """
    Main function to process the log file and return formatted output.

    Args:
        log_file (str): Multi-line string with domain names and their associated numbers.
        min_hits (int): Minimum hit count to include a domain in the output.

    Returns:
        str: Formatted string with domains and their counts.
    """
    domains_count = aggregate_counts(log_file)
    return formatted_output(domains_count, min_hits)


def main():
    formatted_output = count_domains(LOG_FILE_CONTENT, 500)
    print(formatted_output)


if __name__ == "__main__":
    main()
