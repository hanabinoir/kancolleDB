from selenium import webdriver
from selenium.webdriver.common.by import By
import pymysql


# Ship stats initialization
# ship_stats = {
#     "No": "",
#     "Name": "",
#     "Class": "",
#     "Type": "",
#     "Firepower": "",
#     "Torpedo": "",
#     "AA": "",
#     "ASW": "",
#     "LOS": "",
#     "Luck": "",
#     "HP": "",
#     "Armor": "",
#     "Evasion": "",
#     "Speed": "",
#     "Aircraft": "",
#     "Range": "",
#     "Fuel": "",
#     "Ammo": ""
# }
ship_stats = {}

# Set the browser
driver = webdriver.Chrome()

# Set mysql connection
conn = pymysql.connect(
    host="localhost",
    port=3306,
    user="root",
    passwd="",
    db="kancolle",
    charset="utf8"
)
cursor = conn.cursor()


def create_ship_list():
    ship_info_tr = driver.find_element(
        By.XPATH,
        "//span[contains(@id, 'shiplistkai')]/../../../tr"
    )
    ship_info_th = ship_info_tr.find_elements(By.XPATH, "th")
    ship_stats_title = ship_info_tr.find_elements(
        By.XPATH,
        "th/a"
    )
    ship_list_fields = []
    for th in ship_info_th:
        th = th.text.strip()
        if th == "No.":
            th = th[:-1]
        if len(ship_list_fields) < 4:
            ship_list_fields.append(th)

    for title in ship_stats_title:
        title = title.get_attribute("title").strip()
        if "Fuel" in title:
            title = "Fuel"
        if "Ammo" in title:
            title = "Ammo"
        ship_list_fields.append(title)

    varchar_field = {
        "Name",
        "Class",
        "Type",
        "Speed",
        "Range"
    }
    query = "CREATE TABLE IF NOT EXISTS `kancolle`.`ship_list` ("
    for field_name in ship_list_fields:
        field_name = field_name.lower()
        if field_name in varchar_field:
            field_type = "VARCHAR(10)"
        else:
            field_type = "INT(3)"
        field_string = "ship_" + field_name + " " + field_type + ", "
        query += field_string
    query = query[:-2]
    query += ") ENGINE = MyISAM;"
    cursor.execute(query)


def insert_ship_list():
    # Navigate to a tag and its parent row
    ship_list_tbody = driver.find_elements(By.XPATH, "//tbody")
    ship_records = ship_list_tbody[1].find_elements(By.XPATH, "tr")
    record_index = 231

    # Get the values of the fields from the row
    while(record_index < len(ship_records)):
    # for record in ship_records:
        record_index += 1
        print("index: " + str(record_index))

        query = "INSERT INTO `kancolle`.`ship_list` VALUES ("
        value = ""
        for i in range(0, 18):
            try:
                fields = ship_records[record_index].find_elements(By.XPATH, "td")
                if '\n' in fields[i].text:
                    value_list = fields[i].text.split('\n')
                    if '#' in value_list[1]:
                        value_list[1] = value_list[1][1:]
                    query += "'" + value_list[0].strip() + "', '" + value_list[1].strip() + "', "
                    print(value_list[0] + " " + value_list[1])
                else:
                    value = fields[i].text.strip()
                    if i == 1 or i == 2:
                        query += "'" + value + "', 'NA', "
                    else:
                        query += "'" + value + "', "
                    print(value + " ")
            except IndexError:
                print("Table heading detected\n")

        # in case that the row is empty
        query = query[:-2] + ");"
        if value is not "":
            try:
                cursor.execute(query)
            except pymysql.err.IntegrityError as e:
                print("{}, {}".format(e.args[0], e.args[1]))
        print("-----------")


if __name__ == '__main__':
    # Navigate to ship list page
    ship_list_url = "http://kancolle.wikia.com/wiki/Ship_list"
    driver.get(ship_list_url)

    # create_ship_list()
    insert_ship_list()
    cursor.close()
    conn.close()
