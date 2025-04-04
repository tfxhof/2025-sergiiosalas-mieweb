from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# Configurar el driver
driver = webdriver.Chrome(executable_path="path_to_chromedriver")

# Abrir la URL de la app de Panel
driver.get("http://localhost:61788")  # Ajusta la URL según tu configuración

# Esperar a que la página cargue
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "Select materials")))

# 1. Seleccionar el material "Ag" del MultiChoice
multi_choice = driver.find_element(By.NAME, "Select materials")
multi_choice.click()

# Esperar a que las opciones se desplieguen
WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".bk-select-option")))

# Seleccionar "Ag"
ag_option = driver.find_element(By.XPATH, "//div[@class='bk-select-option' and text()='Ag']")
ag_option.click()

# Esperar a que se agregue la opción de "Select page for Ag"
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "Select page for Ag")))

# 2. Seleccionar la página "Johnson" del Select
page_select = driver.find_element(By.NAME, "Select page for Ag")
page_select.click()

# Esperar a que las opciones se desplieguen
WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".bk-select-option")))

# Seleccionar "Johnson"
johnson_option = driver.find_element(By.XPATH, "//div[@class='bk-select-option' and text()='Johnson']")
johnson_option.click()

# 3. Ingresar un valor en el campo de "Radius"
radius_input = driver.find_element(By.NAME, "Radius (nm)")
radius_input.send_keys("100")  # Ejemplo de valor de radio

# Hacer clic en el botón "Confirm radius"
confirm_radius_button = driver.find_element(By.NAME, "Confirm radius")
confirm_radius_button.click()

# 4. Ingresar un valor en el campo de "Refractive index of the medium"
n_surrounding_input = driver.find_element(By.NAME, "Refractive index of the medium")
n_surrounding_input.send_keys("1.5")  # Ejemplo de valor de índice de refracción

# Hacer clic en el botón "Confirm value"
confirm_n_surrounding_button = driver.find_element(By.NAME, "Confirm value")
confirm_n_surrounding_button.click()

# Esperar un momento para que la gráfica se actualice
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".bk-plot-wrapper")))

# A partir de aquí puedes continuar con más interacciones o verificar los resultados

# Cerrar el navegador al final
driver.quit()
