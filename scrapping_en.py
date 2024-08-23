import csv
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from scrapping_fr import timestamp

timestamp = timestamp

# Configuration for headless Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")

# Setup ChromeDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open the initial URL
driver.get("https://www.assyrianlanguages.org/akkadian/index_fr.php")

french_href = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, ".middle a:first-child"))
).get_attribute("href")

print(f"French URL: {french_href}")

# Navigate to the retrieved URL
driver.get(french_href)

# Wait for the second link to be present and retrieve its href attribute
second_href = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, ".widemenulist li:nth-child(2) a"))
).get_attribute("href")

# Récupérer toutes les URLs sous le sélecteur "tbody tr td a"
links = driver.find_elements(By.CSS_SELECTOR, "tbody tr td a")

# Ouvrir un fichier CSV pour écrire les données
with open('resultats_fr.csv', mode='wb') as file:
    file.write('\ufeff'.encode('utf-8'))

with open('resultats_fr.csv', mode='a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter=';', quoting=csv.QUOTE_MINIMAL)
    # Écrire l'en-tête
    # writer.writerow(['Word', 'EN title', 'EN Indication', 'EN Definition'])

    # Parcourir chaque lien, l'ouvrir dans un nouvel onglet, extraire les données, et les écrire dans le fichier CSV
    for link_index in range(len(links)):
        # Afficher l'index du lien / le nombre de liens restants
        print(f"[{link_index}/{len(links)}] - {links[link_index].text}")
        href = links[link_index].get_attribute('href')

        word_title = links[link_index].text

        # Ouvrir un nouvel onglet
        driver.execute_script(f"window.open('{href}');")

        # Passer au nouvel onglet
        driver.switch_to.window(driver.window_handles[-1])

        try:
            # Extraire les données
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".wordlink p:first-child"))
            )
            col2_data = driver.find_element(By.CSS_SELECTOR, ".wordlink p:first-child").text
            col3_data = driver.find_element(By.CSS_SELECTOR, ".wordlink p:nth-child(2)").text
            col4_data = driver.find_element(By.CSS_SELECTOR, ".wordlink p:nth-child(3)").text

            # Écrire les données dans le CSV
            # writer.writerow([word_title, col2_data, col3_data, col4_data])
            print(f"Données extraites : {col2_data}, {col3_data}, {col4_data}")

        except Exception as e:
            print(f"Erreur lors de l'extraction des données de {href} : {e}")
            print(driver.page_source)  # Print the page source for debugging

        # Fermer l'onglet
        driver.close()

        # Revenir à l'onglet original
        driver.switch_to.window(driver.window_handles[0])

# Fermer le navigateur
driver.quit()

# Récupérer un nouveau timestamp
timestamp2 = time.time()

# Calculer le temps écoulé
temps_ecoule = timestamp2 - timestamp

# Afficher le temps écoulé au format HH:MM:SS
print(time.strftime("%H:%M:%S", time.gmtime(temps_ecoule)))