from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf
import requests

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# docker run -t --rm -p 8502:8502 -v C:\Project\potato-disease:/potato-disease tensorflow/serving --rest_api_port=8502 --model_config_file=/potato-disease/models.config
endpoint = "http://localhost:8502/v1/models/potatoes_model:predict"


CLASS_NAMES = ['Potato___Early_blight',
 'Potato___Late_blight',
 'Potato___healthy',
 'Tomato_Bacterial_spot',
 'Tomato_Early_blight',
 'Tomato_Late_blight',
 'Tomato_Leaf_Mold',
 'Tomato_Septoria_leaf_spot',
 'Tomato_Spider_mites_Two_spotted_spider_mite',
 'Tomato__Target_Spot',
 'Tomato__Tomato_YellowLeaf__Curl_Virus',
 'Tomato__Tomato_mosaic_virus',
 'Tomato_healthy']




#For Each Disesae we have heading table and answers
Potato___Early_blight = ['Potato Early Blight',
                         'Clear infected debris from field to reduce inoculum for the next year.Water plants in the morning so plants are wet for the shortest amount of time.Use a drip irrigation system to minimize leaf wetness which provides optimal conditions for fungal growth.Use mulch so spores in soil cannot splash onto leaves from the soil.Rotate to a non-Solanaceous crop for at least three years. The more potato-free years, the less infection.If possible control wild population of Solanaceae. This will decrease the amount of inoculum to infect your plants.Closely monitor field, especially in warm damp weather when it grows fastest, to reduce loss of crop and spray fungicide in time.Plant resistant cultivars.Increase air circulation in rows. Damp conditions allow for optimal growth of A. Solani and the disease spreads more rapidly. This can be achieved by planting farther apart or by trimming leaves.',
                         'The life cycle starts with the fungus overwintering in crop residues or wild members of the family Solanaceae, such as black nightshade.[9] In the spring, conidia are produced. Multicellular conidia are splashed by water or by wind onto an uninfected plant. The conidia infect the plant by entering through small wounds, stomata, or direct penetration. Infections usually start on older leaves close to the ground. The fungus takes time to grow and eventually forms a lesion. From this lesion, more conidia are created and released. These conidia infect other plants or other parts of the same plant within the same growing season. Every part of the plant can be infected and form lesions. This is especially important when fruit or tubers are infected as they can be used to spread the disease.',
                         'Free water is required for Alternaria spores to germinate; spores will be unable to infect a perfectly dry leaf.[3] Alternaria spores germinate within 2 hours over a wide range of temperatures but at 26.6-29.4 °C (80-85 °F) may only take 1/2 hour. Another 3 to 12 hours are required for the fungus to penetrate the plant depending on temperature. After penetration, lesions may form within 2–3 days or the infection can remain dormant awaiting proper conditions [15.5 °C (60 °F) and extended periods of wetness]. Alternaria sporulates best at about 26.6 °C (80 °F) when abundant moisture (as provided by rain, mist, fog, dew, irrigation) is present. Infections are most prevalent on poorly nourished or otherwise stressed plants',
                         'There are numerous fungicides on the market for controlling early blight. Some of the fungicides on the market are (azoxystrobin), pyraclostrobin, Bacillus subtilis, chlorothalonil, copper products, hydrogen dioxide (Hydroperoxyl), mancozeb, potassium bicarbonate, and ziram.[14] Specific spraying regiments are found on the label. Labels for these products should be read carefully before applying.Quinone outside inhibitor (QoIs) fungicides e.g. azoxystrobin are used due to their broad-spectrum activity. However, decreased fungicide sensitivity has been observed in A. solanidue to a F129L (Phenylalanine (F) changed to Leucine at position 129) amino acid substitution']

Potato___Late_blight = ['Potato Late blight',
                        'Information at to be added',
                        'Information at to be added',
                        'Information at to be added',
                        'Information at to be added']
Potato___healthy = ['Potato Plant is Healthy',
                    'Nill',
                    'Nill',
                    'Nill',
                    'Nill'
                    ]
Tomato_Bacterial_spot = ['Tomato Bacterial Spot',
                         'Tomato bacterial spot bacteria can be grown on a variety of media, including nutrient agar, Kings B medium, and XCV agar. These media typically contain nutrients like peptone, beef extract, and agar to support bacterial growth',
                         '1.Crop rotation: One of the key strategies for managing tomato bacterial spot is crop rotation. This involves planting tomatoes in a different field or location each year to reduce the buildup of bacteria in the soil. Crop rotation can also help to prevent the spread of the disease to other fields or crops.<br>2.Removal of infected plant material: Infected plant material should be removed and destroyed as soon as possible to prevent the spread of the bacteria. This includes removing infected leaves, stems, and fruit from the field and disposing of them properly.<br>3.Cleaning of equipment: Tools and equipment used in the field should be cleaned and disinfected between uses to prevent the spread of bacteria. This includes cleaning pruning shears, trellis systems, and other equipment that may come into contact with the plants.<br>4.Use of disease-free seed: Using disease-free seed is important for preventing the introduction of bacterial spot into a field. Seed should be obtained from a reputable source and tested for the presence of the bacteria.<br>5.Avoiding overhead irrigation: Overhead irrigation can promote the spread of tomato bacterial spot by splashing water and bacteria onto the leaves and fruit. Drip irrigation or other methods that minimize the amount of water that comes into contact with the plants are preferred.<br><br>By following good sanitation practices, farmers can reduce the incidence and severity of tomato bacterial spot disease and minimize its impact on their crops.',
                         ' Tomato varieties can be bred for resistance to bacterial spot by selecting for genetic traits that confer resistance. These traits may include the ability to recognize and respond to the bacteria, or the production of antimicrobial compounds that can inhibit bacterial growth. Genetic resistance can be effective, but it may be overcome if the bacteria evolve new virulence factors.',
                         'Chemical control methods, such as the use of copper-based fungicides, can help to manage bacterial spot in the field. However, the effectiveness of these methods can be limited by the development of resistance in the bacteria.'
]

@app.get("/ping")
async def ping():
    return "Hello, I am alive"

def read_file_as_image(data) -> np.ndarray:
    image = np.array(Image.open(BytesIO(data)))
    return image

@app.post("/predict")
async def predict(
    file: UploadFile = File(...)
):
    image = read_file_as_image(await file.read())
    img_batch = np.expand_dims(image, 0)

    json_data = {
        "instances": img_batch.tolist()
    }
    
    response = requests.post(endpoint, json=json_data)
    prediction = np.array(response.json()["predictions"][0])

    idx = np.argmax(prediction)
    predicted_class = CLASS_NAMES[np.argmax(prediction)]
    confidence = np.max(prediction)

    classnames_arr = [Potato___Early_blight,Potato___Late_blight,Potato___healthy]
    

    return {
        "class":predicted_class,
        "confidence":float(confidence),
        "culture":classnames_arr[idx][1],
        "resistance":classnames_arr[idx][3],
        "chemicalcontrol":classnames_arr[idx][4],
        "sanitation":classnames_arr[idx][2]
    }
    

if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=8000)