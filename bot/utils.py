
def remove_non_service_data(data: dict):
    """
        Removes all data that are not marked as service.
        :param: data
        :return: only service data (clean data).
        Example:
            instead of using:
                await state.reset_data()
            use:
                await state.set_data(remove_non_service_data(data))
    """
    service_data = {'_time': data['_time']}

    data.clear()
    return service_data


def generate_topic_str(topics: dict) -> str:
    topics_str = ""
    for t in topics.keys():
        tag = topics[t] + "::" + t + "; "
        topics_str += tag

    return topics_str
