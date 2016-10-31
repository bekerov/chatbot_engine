
def find_city(query):

    city_list = ["서울","대구","인천","부산","도쿄", "샌프란시스코","뉴욕"]

    target_city = None

    for city in city_list:
        if city in query:
            target_city = city

    return target_city


