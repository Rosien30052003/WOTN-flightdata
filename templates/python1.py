from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Đường dẫn đến file Excel
excel_file_path = 'C:/Users/chibi/Desktop/code/Results.xlsx'

# Đọc dữ liệu từ file Excel khi server khởi động
flight_data = pd.read_excel(excel_file_path)
flight_data.columns = [col.strip() for col in flight_data.columns]  # Xóa khoảng trắng trong tên cột

@app.route('/', methods=['GET'])
def index():
    flight_number = request.args.get('flight_number')
    show_more = request.args.get('show_more') == 'true'  # Lấy tham số 'show_more'
    search_result = None
    additional_info = None

    if flight_number and flight_data is not None:
        # Lọc dữ liệu dựa trên số hiệu chuyến bay
        filtered_data = flight_data[flight_data['Flight Number'] == flight_number]
        
        # Kiểm tra nếu có kết quả phù hợp và chuyển thành danh sách dictionary
        if not filtered_data.empty:
            search_result = filtered_data.to_dict(orient="records")
        else:
            search_result = []  # Nếu không có kết quả phù hợp, trả về danh sách rỗng

        # Nếu người dùng nhấn nút "xem đường bay", lấy thông tin về đường bay
        if show_more:
            # Lấy các cột thông tin về đường bay
            route_columns = ['N1', 'N2', 'N3', 'N4', 'N5', 'N6', 'N7', 'N8', 'N9', 'N10', 'N11', 'N12', 'N13']
            additional_info = filtered_data[route_columns].to_dict(orient="records")

    # Render HTML template với kết quả tìm kiếm
    return render_template('web.html', search_result=search_result, additional_info=additional_info, flight_number=flight_number)

if __name__ == '__main__':
    app.run(debug=True)