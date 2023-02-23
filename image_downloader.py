import os
import urllib.request
import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

DRIVER_PATH = "chromedriver.exe"
IMAGE_DIR = "images"

def download_images(selected_tags):
    # Khởi tạo đối tượng WebDriver cho Chrome
    driver = webdriver.Chrome(DRIVER_PATH)

    # Mở trang web Google Images trên từng tab và tìm kiếm ảnh của từng tag
    for tag in selected_tags:
        # Tạo thư mục tag trong thư mục images nếu chưa tồn tại
        path = os.path.join(IMAGE_DIR, tag)
        if not os.path.exists(path):
            os.makedirs(path)

        # Mở một tab mới và chuyển sang tab đó
        driver.execute_script("window.open('https://www.google.com/imghp', 'new_window')")
        driver.switch_to.window(driver.window_handles[-1])

        # Tìm kiếm ảnh của tag hiện tại
        search_box = driver.find_element(By.NAME, 'q')
        search_box.send_keys(tag)
        search_box.submit()

        # Sử dụng hàm WebDriverWait để chờ đợi tải các ảnh
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'img.rg_i'))) # delay for a maximum of 10 seconds
        except:
            st.write('Could not download images for', tag)
            continue

        # Lưu 10 ảnh đầu tiên vào thư mục tag
        images = driver.find_elements(By.CSS_SELECTOR, 'img.rg_i')[:10]
        for i, image in enumerate(images):
            url = image.get_attribute('src')
            filename = f'{tag}_{i}.jpg'
            filepath = os.path.join(path, filename)
            urllib.request.urlretrieve(url, filepath)

    # Đóng trình duyệt và kết thúc chương trình
    driver.quit()
    st.write('Images downloaded successfully!')

def main():
    st.set_page_config(page_title="Image Downloader", page_icon=":camera:", layout="wide")
    # Tạo container để chứa header
    header_container = st.container()

    # Sử dụng layout để canh giữa header
    col, _ = st.columns([1, 2])

    # Thêm title và text vào container
    with header_container:
        with col:
            st.title("Image Downloader")
            st.markdown("---")

    tag_container = st.container()
    with tag_container:
        st.write("Add tags to download images")
        tags_input = st.text_input("", key="tag_input").strip().split(",")
        tags_input = [x for x in tags_input if x != ""]
    # Hiển thị các tag
    col1, _ = st.columns([1,1])
    col1.write("Selected tags")
    tags_html = "".join([f"<span style='color:#ff33cc; font-weight:bold; font-size:20px'>#{tag}</span>" for tag in tags_input])
    col1.markdown(tags_html, unsafe_allow_html=True)

    if st.button("Download images"):
        if tags_input:
            download_images(tags_input)
        else:
            st.write("No tags selected.")


if __name__ == "__main__":
    main()
