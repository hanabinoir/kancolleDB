from selenium import webdriver
from selenium.webdriver.common.by import By
import pymysql


# Ship stats initialization
ship_stats = {
    "No": "",
    "Name": "",
    "Class": "",
    "Type": "",
    "Firepower": "",
    "Torpedo": "",
    "AA": "",
    "ASW": "",
    "LOS": "",
    "Luck": "",
    "HP": "",
    "Armor": "",
    "Evasion": "",
    "Speed": "",
    "Aircraft": "",
    "Range": "",
    "Fuel": "",
    "Ammo": ""
}

# Set the browser
driver = webdriver.Chrome()

# Set mysql connection
conn = pymysql.connect(
    host="localhost",
    port=3306,
    user="root",
    passwd="",
    db="kancolle"
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
        "ship_name",
        "ship_class",
        "ship_type",
        "ship_speed",
        "ship_range"
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
    ship_stats["Name"] = driver.find_element(By.XPATH, "//span[contains(@id, 'shiplistkai')]/a")

    ship_records = ship_stats["Name"].find_elements(By.XPATH, "../../../../tr")

    # Get the values of the fields from the row
    for record in ship_records:
        fields = record.find_elements(By.XPATH, "td")
        try:
            ship_stats["No"] = fields[0].text.strip()
            ship_stats["Name"] = fields[1].find_element(
                By.XPATH,
                "/span[contains(@id, 'shiplistkai')]/a"
            ).text.strip()
            ship_stats["Class"] = fields[2].text.split("\n")[0].strip()
            ship_stats["Type"] = fields[3].text.strip()
            ship_stats["Firepower"] = fields[4].text.strip()
            ship_stats["Torpedo"] = fields[5].text.strip()
            ship_stats["AA"] = fields[6].text.strip()
            ship_stats["ASW"] = fields[7].text.strip()
            ship_stats["LOS"] = fields[8].text.strip()
            ship_stats["Luck"] = fields[9].text.strip()
            ship_stats["HP"] = fields[10].text.strip()
            ship_stats["Armor"] = fields[11].text.strip()
            ship_stats["Evasion"] = fields[12].text.strip()
            ship_stats["Speed"] = fields[13].text.strip()
            ship_stats["Aircraft"] = fields[14].text.strip()
            ship_stats["Range"] = fields[15].text.strip()
            ship_stats["Fuel"] = fields[16].text.strip()
            ship_stats["Ammo"] = fields[17].text.strip()
            for key in ship_stats:
                print(key + ": " + ship_stats[key] + "\n")
        except IndexError:
            print("Table heading detected\n")


if __name__ == '__main__':
    # Navigate to ship list page
    ship_list_url = "http://kancolle.wikia.com/wiki/Ship_list"
    driver.get(ship_list_url)

    create_ship_list()
    # insert_ship_list()
    cursor.close()
    conn.close()