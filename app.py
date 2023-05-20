from flask import Flask, render_template_string, request
import qrcode
import base64

app = Flask(__name__)

html_template = '''
<!DOCTYPE html>
<html>
<head>
    <title>D.S. Photographic Art Society</title>
    <link rel="icon" href="https://z-p3-scontent.fcmb9-1.fna.fbcdn.net/v/t39.30808-6/323415179_1194657114479909_332227155832890697_n.jpg?_nc_cat=110&cb=99be929b-59f725be&ccb=1-7&_nc_sid=09cbfe&_nc_eui2=AeFaAthQzvgGFWHwkC3Eb7SDDZP5LX6ZcG0Nk_ktfplwbVsd8dwGlD08rS5jL-L0kg-HEDovklYLPtoAM__VKIwP&_nc_ohc=fgYrYA1-5bIAX-2IZfX&_nc_zt=23&_nc_ht=z-p3-scontent.fcmb9-1.fna&oh=00_AfAzawbTh8DnRG05PmhTUSlQLvlsaewtnyVSOIdmNsX34A&oe=646ED2FB">

    <style>
        * {
            box-sizing: border-box;
        }

        body {
            background-image: url(https://wallpapercave.com/wp/wp1933338.jpg);
            font-family: Arial, sans-serif;
            background-size: cover;
            background-position: center;
            margin: 0;
            padding: 20px;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }

        .container {
            max-width: 400px;
            background-color: #fff;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }

        h1, h3 {
            text-align: center;
            margin-top: 0;
        }

        form {
            display: flex;
            flex-direction: column;
        }

        input[type="text"],
        input[type="number"],
        input[type="tel"],
        input[type="email"],
        input[type="submit"] {
            margin-bottom: 16px;
            padding: 8px;
            border-radius: 4px;
            border: 1px solid #ccc;
        }

        input[type="submit"] {
            background-color: #000296;
            color: #fff;
            border: none;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }

        input[type="submit"]:hover {
            background-color: #0e0041;
        }

        img {
            display: block;
            margin-top: 20px;
            max-width: 100%;
            height: auto;
            margin-left: auto;
            margin-right: auto;
        }

        /* Media queries for responsive design */
        @media screen and (max-width: 480px) {
            .container {
                padding: 20px;
            }
        }

        @media screen and (max-width: 768px) {
            .container {
                max-width: 600px;
            }
        }

        @media screen and (max-width: 992px) {
            .container {
                max-width: 800px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>D.S. Photographic Art Society</h1>
        <h3>Collecting Photographer's personal details</h3>
        <form method="POST">
            <input type="text" id="name" name="name" placeholder="Enter your Name:" required>
            <input type="number" id="age" name="age" placeholder="Enter your Age:" required>
            <input type="tel" id="phone_number" name="phone_number" placeholder="Enter your Phone Number:" required>
            <input type="email" id="e_mail" name="e_mail" placeholder="Enter your E-mail:" required>
            <input type="tel" id="whatsapp_number" name="whatsapp_number" placeholder="Enter your Whatsapp Number:" required>
            <input type="submit" value="Generate QR Code">
        </form>

        {% if qr_code_image %}
            <h2>QR Code:</h2>
            <img src="{{ qr_code_image }}" alt="QR Code">
        {% endif %}
    </div>
</body>
</html>

'''

@app.route('/', methods=['GET', 'POST'])
def generate_qr_code():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        phone_number = request.form['phone_number']
        e_mail = request.form['e_mail']
        whatsapp_number = request.form['whatsapp_number']

        data = f"Name: {name}\nAge: {age}\nPhone Number: {phone_number}\nE-mail: {e_mail}\nWhatsApp Number: {whatsapp_number}"

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )

        qr.add_data(data)
        qr.make(fit=True)

        qr_image = qr.make_image(fill_color="black", back_color="white")

        # Convert the QR code image to base64 string
        qr_code_base64 = base64.b64encode(qr_image.tobytes()).decode('utf-8')

        # Format the base64 string as a data URL
        qr_code_data_url = f"data:image/png;base64,{qr_code_base64}"

        image_path = "qrcode.png"
        qr_image.save(image_path)

        return render_template_string(html_template, qr_code_image=qr_code_data_url)

    return render_template_string(html_template)

if __name__ == '__main__':
    app.run(debug=True)
