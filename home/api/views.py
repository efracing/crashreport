import base64, pdfkit
from io import BytesIO
from datetime import datetime
from PIL import Image, ExifTags

from jinja2 import Template
from rest_framework import status
from django.http import FileResponse
from rest_framework.views import APIView
from home.api.serializers import CrashReportSerializer


class BuildPdfAPIView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = CrashReportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = dict(serializer.data)

        buffer, filename = self.crash_report(data)
        response = FileResponse(buffer, filename=filename, as_attachment=True)

        return FileResponse(response, status=status.HTTP_200_OK)


    def crash_report(self, data):
        counter = 0
        for index, group in enumerate(data['image_groups']):
            data['image_groups'][index]['mimages'] = []
            for img in group['images']:
                # base64img = self.correct_image_orientation(img)
                counter += 1
                data['image_groups'][index]['mimages'].append({'image': img, 'counter': counter})
            if (counter + 1) % 2 == 0:
                counter += 1
                data['image_groups'][index]['mimages'].append({'image': None, 'counter': counter})
            if not group['notes'].strip():
                data['image_groups'][index]['notes'] = None

        print(data)

        with open('home/report/crash/header.html', 'r') as f:
            content = f.read()
        template = Template(content)
        content = template.render(data)
        with open('home/report/crash/head.html', 'w') as f:
            f.write(content)

        with open('home/report/crash/template.html', 'r') as f:
            content = f.read()
        template = Template(content)
        content = template.render(data)
        with open('home/report/crash/temp.html', 'w') as f:
            f.write(content)

        options = {
            'page-size': 'A4',
            'header-html': 'home/report/crash/head.html',
            'footer-html': 'home/report/crash/footer.html',
            'enable-local-file-access': '',
        }
        pdf = pdfkit.from_string(content, options=options)

        buffer = BytesIO(pdf)
        buffer.seek(0)

        now = datetime.now()
        filename = f'crash-report_{now.date()}.xlsx'

        return buffer, filename


    def correct_image_orientation(self, base64_string):
        try:
            # Decodifica la stringa base64
            image_data = base64.b64decode(base64_string)
            image = Image.open(BytesIO(image_data))
            
            # Estrarre i metadati EXIF
            exif = image._getexif()
            if exif is not None:
                for tag, value in exif.items():
                    decoded = ExifTags.TAGS.get(tag, tag)
                    if decoded == 'Orientation':
                        orientation = value
                        # Applicare la rotazione in base all'orientamento EXIF
                        if orientation == 3:
                            image = image.rotate(180, expand=True)
                        elif orientation == 6:
                            image = image.rotate(270, expand=True)
                        elif orientation == 8:
                            image = image.rotate(90, expand=True)
                        break
            
            # Salva l'immagine corretta in un oggetto BytesIO
            buffered = BytesIO()
            image.save(buffered, format=image.format)
            
            # Converti l'immagine corretta in una stringa base64
            corrected_base64_string = base64.b64encode(buffered.getvalue()).decode('utf-8')
            return corrected_base64_string

        except Exception as e:
            print(f'Errore nella correzione dell\'immagine: {e}')
            return None
