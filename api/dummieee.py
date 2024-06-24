from google.cloud import storage
import tensorflow as tf
from PIL import Image
import numpy as np

from flask import Flask,jsonify

BUCKET_NAME = "disease-classification" 
class_names = ['Pepper__bell___Bacterial_spot',
'Pepper__bell___healthy',
'Potato___Early_blight',
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
Pepper__bell___Bacterial_spot = ['Pepper Bell Bacterial Spot',
                                 'Bell pepper bacterial spot is a disease caused by the bacteria Xanthomonas campestris pv. vesicatoria. It can affect all parts of the plant including leaves, stems, fruit, and seeds. The disease is characterized by the appearance of small, water-soaked spots on the leaves and stems that eventually turn brown and necrotic. On the fruit, the spots may be slightly sunken and have a raised, scabby appearance. The disease can reduce the yield and quality of the fruit and can also cause defoliation and weaken the plant.',
                                 'There are bell pepper cultivars that have been developed with resistance to bacterial spot. These cultivars have been bred to have genetic traits that make them less susceptible to the bacteria that cause the disease. However, its important to note that no cultivar is completely immune to bacterial spot, and even resistant cultivars may still become infected under certain environmental conditions or if there is a particularly virulent strain of the bacteria present. Therefore, growers should still implement appropriate management practices to minimize the risk of bacterial spot.',
                                 'Bell pepper bacterial spot can be controlled with various chemical measures. Copper-based fungicides and bactericides, such as copper hydroxide and copper sulfate, are commonly used to manage bacterial spot on bell peppers. Chlorothalonil and mancozeb are other fungicides that can be effective against bacterial spot.',
                                 'Bacterial spot disease of bell peppers can be managed by following good sanitation practices. Some of the sanitation measures that can help control the disease include:1)	Crop rotation2)	Removing infected plant debris 3)	Disinfecting tools and equipment 4)	Controlling weeds 5)	Minimizing water splash These sanitation practices, along with other management strategies such as planting resistant varieties and using copper-based fungicides, can help control bacterial spot disease in bell peppers.']

Pepper__bell___healthy = ['Pepper Bell Healthy',
                          'Bell pepper healthy culture refers to the cultivation of bell peppers in a manner that minimizes the risk of diseases and pests. This includes proper crop rotation, maintaining healthy soil, using disease-resistant varieties, ensuring proper watering and drainage, and implementing integrated pest management practices. By following these cultural practices, growers can reduce the risk of diseases and pests and promote the overall health of the bell pepper crop.',
                          'Bell peppers can be bred to have resistance to certain diseases or pests, such as bacterial spot or aphids, through traditional breeding methods or genetic modification. However, the specific resistance of a particular bell pepper variety will depend on the breeding program or genetic modifications used to develop it.',
                          'Plant is healthy no chemical control required',
                          'Bell pepper healthy sanitation refers to practices and measures aimed at preventing or minimizing the occurrence and spread of diseases, pests, and other harmful factors that can affect the growth and yield of bell pepper plants. Sanitation measures for bell pepper plants include proper site selection and preparation, soil fertility management, proper spacing, use of clean seeds and planting materials, removal of infected plant debris and weeds, regular monitoring and inspection of plants, and appropriate use of pesticides and other control methods when necessary. These practices can help to maintain a healthy growing environment for bell pepper plants, reduce the risk of disease and pest problems, and promote optimal growth and yield.']

Potato___Early_blight = ['Potato Early Blight',
                         'Clear infected debris from field to reduce inoculum for the next year.Water plants in the morning so plants are wet for the shortest amount of time.Use a drip irrigation system to minimize leaf wetness which provides optimal conditions for fungal growth.Use mulch so spores in soil cannot splash onto leaves from the soil.Rotate to a non-Solanaceous crop for at least three years. The more potato-free years, the less infection.If possible control wild population of Solanaceae. This will decrease the amount of inoculum to infect your plants.Closely monitor field, especially in warm damp weather when it grows fastest, to reduce loss of crop and spray fungicide in time.Plant resistant cultivars.Increase air circulation in rows. Damp conditions allow for optimal growth of A. Solani and the disease spreads more rapidly. This can be achieved by planting farther apart or by trimming leaves.',
                         'The life cycle starts with the fungus overwintering in crop residues or wild members of the family Solanaceae, such as black nightshade.[9] In the spring, conidia are produced. Multicellular conidia are splashed by water or by wind onto an uninfected plant. The conidia infect the plant by entering through small wounds, stomata, or direct penetration. Infections usually start on older leaves close to the ground. The fungus takes time to grow and eventually forms a lesion. From this lesion, more conidia are created and released. These conidia infect other plants or other parts of the same plant within the same growing season. Every part of the plant can be infected and form lesions. This is especially important when fruit or tubers are infected as they can be used to spread the disease.',
                         'Free water is required for Alternaria spores to germinate; spores will be unable to infect a perfectly dry leaf.[3] Alternaria spores germinate within 2 hours over a wide range of temperatures but at 26.6-29.4 °C (80-85 °F) may only take 1/2 hour. Another 3 to 12 hours are required for the fungus to penetrate the plant depending on temperature. After penetration, lesions may form within 2–3 days or the infection can remain dormant awaiting proper conditions [15.5 °C (60 °F) and extended periods of wetness]. Alternaria sporulates best at about 26.6 °C (80 °F) when abundant moisture (as provided by rain, mist, fog, dew, irrigation) is present. Infections are most prevalent on poorly nourished or otherwise stressed plants',
                         'There are numerous fungicides on the market for controlling early blight. Some of the fungicides on the market are (azoxystrobin), pyraclostrobin, Bacillus subtilis, chlorothalonil, copper products, hydrogen dioxide (Hydroperoxyl), mancozeb, potassium bicarbonate, and ziram.[14] Specific spraying regiments are found on the label. Labels for these products should be read carefully before applying.Quinone outside inhibitor (QoIs) fungicides e.g. azoxystrobin are used due to their broad-spectrum activity. However, decreased fungicide sensitivity has been observed in A. solanidue to a F129L (Phenylalanine (F) changed to Leucine at position 129) amino acid substitution']

Potato___Late_blight = ['Potato Late blight',
                        "Late blight of potatoes is caused by a pathogenic fungus called Phytophthora infestans. It is a potentially devastating disease that primarily affects potato crops but can also be seen in members of the Solanaceae family, including tomatoes, petunias and hairy nightshades. Late blight can cause significant yield losses and can be difficult to control",
                        "Potato late blight is a fungal disease caused by Phytophthora infestans. Some potato varieties have a natural resistance to blight, while others are bred to resist blight by transferring genes from wild relatives of potatoes. Blight-resistant potatoes may avoid infection even when the fungus is present in the soil or nearby crops. Some examples of blight-resistant potatoes are Carolus, Alouette, Solanum Americanum, IdaRose, Red Cloud, Sarpo Mira, Cara, and Valor. Choosing blight-resistant potatoes is one of the best ways to avoid blight in your potatoes.",
                        "Late blight of potato is a serious disease that can cause significant yield losses if not managed properly. Chemical control is one of the most effective ways to manage this disease. Some of the fungicides that can be used for chemical control of late blight of potato include Ridomil (0.2%), Dithane M-45, Copper oxichloride @ 3-4 g/L for 2-3 times at 10-15 days interval. Tuber should be treated by dipping in Bordeaux mixture (1%) or other fungicides e.g. Dithane M-45 (0.2%) for 3-5 minutes.",
                        "Sanitation is one of the most important techniques for management of the late blight of potato disease. Sanitation in the storage area can help prevent the spread of the disease. The potato tubers must be treated with 1: 1000 mercuric chloride solution for 90 minutes prior to storage. This helps in inhibiting the growth of mycelium."]
Potato___healthy = ['Potato Plant is Healthy',
                    "When it comes to cultivating healthy potatoes, there are several things you can do to increase your harvest. For instance, you should choose the right potatoes and spot to grow them. You should also prepare your growing area and amend the soil if the pH is not ideal1. Chitting potatoes can also help get them off to a good start. Additionally, you should get your timing right when planting out and get the spacing right. Adding fertility when planting out seed potatoes can also help improve their health.Potatoes can be cultivated in a variety of soil types including loamy soil, sandy loam, silt loam, and clay soil. Soil should be loose in order to provide less resistance to tuber enlargement. The soil must be fertile and well-drained. Potato cultivation requires acidic soil with a pH range of 4.8 to 5.42. The potato is classified as a cool-weather crop. Potato vegetative growth is best at temperatures of 24 degrees Celsius, and tuber growth is best at temperatures of 20 degrees Celsius.",
                    "There are several ways to increase the resistance of potato plants to pests and diseases. One way is to choose varieties that resist the pests and diseases you most expect. Another way is to add compost and cover crops to build fertile soil to support strong plant growth and help increase the diversity of soil microorganisms, building naturally disease-suppressing soil. Crop rotation can also reduce the chances of pests and diseases carrying over from one crop to the next. Good sanitation practices can also help reduce pest and disease pressure.",
                    "Chemical control methods are often combined with biocontrol agents to effectively fight potato pathogens. The external appearance and quality of table potatoes are determined, among other factors, by the health status of the plants during the growing season. Potatoes of the very early cultivar Rosara were grown in experimental plots. The experiment involved the following treatments: 1) biological control − mycorrhizal Glomus spp. inoculum was applied to the roots, − tubers were dressed and plants were sprayed with Polyversum three times during the growing season.2) chemical control – at two-week intervals, plants were sprayed with the following fungicides: Infinito 687.5 SC and Tanos 50 WG, Valbon 72 WG and Tanos 50 WG. During the growing season, the severity of late blight and early blight was evaluated on a nine-point scale. The symptoms of infections caused by Phytophthora infestans and Alternaria spp. were significantly reduced in the treatment which used the integrated chemical and biological control.",
                    "Sanitation is critical to prevent plant diseases in potatoes. It is important to disinfect surfaces such as greenhouse benches, potting stations, etc. before transplant production season. Removing plant debris by collecting, bagging and removing is also important. It is also important to remove infected plants as soon as symptoms appear by collecting, bagging and removing from greenhouse premises. Disinfecting knives, shears and other harvesting tools and frequent hand-washing with clean water and soap are also important."
                    ]
Tomato_Bacterial_spot = ['Tomato Bacterial Spot',
                         'Tomato bacterial spot bacteria can be grown on a variety of media, including nutrient agar, Kings B medium, and XCV agar. These media typically contain nutrients like peptone, beef extract, and agar to support bacterial growth',
                         '1.Crop rotation: One of the key strategies for managing tomato bacterial spot is crop rotation. This involves planting tomatoes in a different field or location each year to reduce the buildup of bacteria in the soil. Crop rotation can also help to prevent the spread of the disease to other fields or crops.<br>2.Removal of infected plant material: Infected plant material should be removed and destroyed as soon as possible to prevent the spread of the bacteria. This includes removing infected leaves, stems, and fruit from the field and disposing of them properly.<br>3.Cleaning of equipment: Tools and equipment used in the field should be cleaned and disinfected between uses to prevent the spread of bacteria. This includes cleaning pruning shears, trellis systems, and other equipment that may come into contact with the plants.<br>4.Use of disease-free seed: Using disease-free seed is important for preventing the introduction of bacterial spot into a field. Seed should be obtained from a reputable source and tested for the presence of the bacteria.<br>5.Avoiding overhead irrigation: Overhead irrigation can promote the spread of tomato bacterial spot by splashing water and bacteria onto the leaves and fruit. Drip irrigation or other methods that minimize the amount of water that comes into contact with the plants are preferred.<br><br>By following good sanitation practices, farmers can reduce the incidence and severity of tomato bacterial spot disease and minimize its impact on their crops.',
                         ' Tomato varieties can be bred for resistance to bacterial spot by selecting for genetic traits that confer resistance. These traits may include the ability to recognize and respond to the bacteria, or the production of antimicrobial compounds that can inhibit bacterial growth. Genetic resistance can be effective, but it may be overcome if the bacteria evolve new virulence factors.',
                         'Chemical control methods, such as the use of copper-based fungicides, can help to manage bacterial spot in the field. However, the effectiveness of these methods can be limited by the development of resistance in the bacteria.'
]

Tomato_Early_blight = [
    'Tomato Early Blight',
    'Tomato early blight (Alternaria solani) is a fungal disease that affects tomato plants. It is important to take measures to prevent the spread of the disease and to control it if it appears.One way to culture the fungus responsible for tomato early blight is to obtain a sample from an infected plant and place it on a sterile nutrient agar plate. The plate should be incubated at a temperature of 25-28°C with a relative humidity of 80-85%. After a few days, the fungus should grow and produce characteristic dark, concentric lesions on the plate.',
    "Tomato plants can develop resistance to early blight through breeding and genetic selection. There are several varieties of tomato plants that have been bred to have resistance to early blight, such as 'Mountain Magic', 'Mountain Merit', 'Defiant', and 'Legend'.Chemical control of tomato early blight can be effective in reducing disease severity when used in combination with cultural practices. However, it is important to follow the manufacturer's instructions when using fungicides, as overuse or misuse can lead to the development of fungicide-resistant strains of the fungus.",
    "Free water is required for Alternaria spores to germinate; spores will be unable to infect a perfectly dry leaf.[3] Alternaria spores germinate within 2 hours over a wide range of temperatures but at 26.6-29.4 °C (80-85 °F) may only take 1/2 hour. Another 3 to 12 hours are required for the fungus to penetrate the plant depending on temperature. After penetration, lesions may form within 2–3 days or the infection can remain dormant awaiting proper conditions [15.5 °C (60 °F) and extended periods of wetness]. Alternaria sporulates best at about 26.6 °C (80 °F) when abundant moisture (as provided by rain, mist, fog, dew, irrigation) is present. Infections are most prevalent on poorly nourished or otherwise stressed plants",
    'Sanitation is an important part of managing tomato early blight. Proper sanitation can help prevent the spread of the fungus to healthy plants and reduce the severity of the disease.'
]

Tomato_Late_blight = [
    'Tomato Late Blight',
    'Tomato late blight (Phytophthora infestans) culture refers to the process of growing and maintaining the fungal pathogen responsible for causing late blight in tomato plants. The culture is typically grown in a laboratory setting for research purposes or to test the effectiveness of fungicides and other treatments for late blight.',
    "Tomato plants can develop resistance to late blight through breeding and genetic selection. There are several varieties of tomato plants that have been bred to have resistance to late blight, such as 'Mountain Magic', 'Mountain Merit', 'Defiant', and 'Legend'. These resistant varieties typically carry one or more resistance genes that allow them to fend off the fungus.",
    'Chemical control is often used to manage tomato late blight, especially when resistant varieties are not available or not effective. The most effective fungicides for controlling late blight are those that contain a systemic fungicide, which can penetrate into the plant tissue and provide long-lasting protection',
    'Chemical control is often used to manage tomato late blight, especially when resistant varieties are not available or not effective. The most effective fungicides for controlling late blight are those that contain a systemic fungicide, which can penetrate into the plant tissue and provide long-lasting protection'
]

Tomato_Leaf_Mold = [
    'Tomato Leaf Mold',
    "Tomato leaf mold (Passalora fulva) is a fungal disease that affects tomato plants. To culture tomato leaf mold, a sample of infected plant tissue, such as a leaf with visible symptoms of the disease, is collected and placed onto a sterile nutrient agar medium. The culture is then incubated under specific temperature and humidity conditions to promote fungal growth.",
    "There are tomato varieties that have been bred to have resistance to tomato leaf mold (Passalora fulva). These varieties have genetic traits that allow them to fend off the fungus that causes the disease. Some of the tomato varieties that have shown resistance to leaf mold include 'Iron Lady', 'Mountain Magic', 'Mountain Merit', 'Plum Regal', and 'Defiant'.",
    "Tomato leaf mold (Passalora fulva) can be controlled using chemical fungicides. The most commonly used fungicides for tomato leaf mold are chlorothalonil, copper fungicides, and mancozeb. These fungicides are applied as a foliar spray and work by preventing the growth and spread of the fungus.",
    "Tomato leaf mold (Passalora fulva) sanitation refers to the set of practices aimed at preventing and controlling the spread of the disease. These include: 1) Removing infected plant debris 2) Crop rotation 3) Proper watering 4) Good air circulation By implementing these sanitation practices, the severity and spread of tomato leaf mold can be reduced, and the likelihood of crop losses can be minimized."
]
Tomato_Septoria_leaf_spot = [
    'Tomato Septoria Leaf Spot',
    "Tomato Septoria Leaf Spot (Septoria lycopersici) is a fungal disease that affects tomatoes worldwide. The fungus can survive on infected plant debris in the soil for up to two years and can spread via water, wind, and insects. The disease is most severe in warm and humid conditions, typically in late summer or early fall. Symptoms of the disease include small, dark spots with gray centers and yellow halos on the lower leaves, which can eventually spread to the upper parts of the plant.",
    "Tomato Septoria Leaf Spot resistance refers to the ability of a tomato plant to resist or tolerate infection by the fungus Septoria lycopersici, which causes the disease. Some tomato varieties have been bred to have genetic resistance to the fungus, meaning that they are less likely to become infected or are able to tolerate the infection without suffering severe damage or yield losses.",
    "Chemical control of Tomato Septoria Leaf Spot (Septoria lycopersici) can be an effective way to manage the disease, but it should be used in conjunction with other management practices to achieve the best results. Fungicides are most effective when used preventatively before symptoms of the disease appear, and should be applied according to the label instructions.",
    "Tomato Septoria Leaf Spot sanitation refers to a set of practices that aim to prevent the spread and reduce the impact of the disease caused by the fungus Septoria lycopersici. Sanitation practices are essential for managing this disease and can be used in conjunction with other management practices, including chemical control and genetic resistance."
]
Tomato_Spider_mites_Two_spotted_spider_mite = [
    'Tomato Spider Mites Two Spotted Spider Mite',
    "Two-spotted spider mites (Tetranychus urticae) are a common pest of tomato plants. They are tiny arachnids that feed on the plant cells by piercing the leaves and sucking out the juices. This can lead to yellowing of the leaves, stunting of growth, and in severe cases, defoliation and death of the plant.",
    "There are some tomato varieties that have been found to be resistant or tolerant to two-spotted spider mites (Tetranychus urticae), meaning that they are less likely to become infested or experience severe damage. Resistance is often based on genetic traits and may vary between different tomato cultivars.",
    "Chemical control is one method for managing two-spotted spider mites (Tetranychus urticae) on tomato plants. However, it is important to use chemicals as a last resort, and to follow label instructions carefully to avoid damage to the tomato plant and unintended harm to non-target organisms.",
    "Sanitation practices can also be effective in managing two-spotted spider mites (Tetranychus urticae) on tomato plants. These practices involve removing and destroying infested plant material and debris, as well as maintaining a clean growing environment to prevent spider mite populations from building up."
]
Tomato__Target_Spot = [
    'Tomato Target Spot',
    "Tomato target spot, also known as early blight, is a fungal disease caused by the pathogen Alternaria solani. It can affect all parts of the tomato plant, including leaves, stems, and fruit, and can cause significant yield losses if left untreated.",
    "There are tomato cultivars that have been bred for resistance to tomato target spot (early blight), which can be a useful tool in managing this disease. These cultivars have genetic traits that allow them to resist or tolerate infection from the Alternaria solani pathogen that causes tomato target spot.",
    "Chemical control can be an effective way to manage tomato target spot (early blight) on tomato plants. Fungicides are available that can help to prevent or reduce the severity of this disease, but it's important to note that overuse of fungicides can lead to the development of resistant fungal strains.",
    "Sanitation practices can also be effective in managing tomato target spot (early blight) on tomato plants. These practices involve removing and destroying infected plant material and debris, as well as maintaining a clean growing environment to prevent fungal spores from building up."
]
Tomato__Tomato_YellowLeaf__Curl_Virus = [
    'Tomato Yellow Leaf Curl Virus',
    "The culture of Tomato Yellow Leaf Curl Virus (TYLCV) refers to the conditions in which the virus can thrive and reproduce. TYLCV is a plant virus that can infect tomato plants, as well as other plants in the Solanaceae family, such as peppers and eggplants.The virus is transmitted by the sweet potato whitefly (Bemisia tabaci), which feeds on the sap of infected plants and then spreads the virus to healthy plants. TYLCV can survive in plant debris and soil for extended periods of time, and can be carried over from one growing season to the next.",
    "Tomato Yellow Leaf Curl Virus (TYLCV) can cause significant yield losses in tomato crops, particularly in tropical and subtropical regions. Breeding programs have developed tomato cultivars that are resistant to TYLCV, and these cultivars can be effective in reducing the impact of the disease.Resistance to TYLCV is conferred by a single dominant gene, known as the Ty gene. Tomato plants that carry the Ty gene are able to resist infection by the virus, although they may still show some symptoms of the disease. However, it is important to note that no cultivar is completely resistant to TYLCV, and that the effectiveness of resistance can vary depending on the specific strain of the virus that is present.",
    "Chemical control of Tomato Yellow Leaf Curl Virus (TYLCV) is challenging, as there are no specific chemicals that can target the virus directly. Instead, management of TYLCV typically involves the use of insecticides to control the whitefly vector that transmits the virus.",
    "Tomato Yellow Leaf Curl Virus (TYLCV) sanitation practices involve the implementation of measures to reduce the spread and impact of the virus. This includes removing infected plants, eliminating alternate hosts and controlling weeds, maintaining a clean growing area, and monitoring for whiteflies."
]
Tomato__Tomato_mosaic_virus = [
    "Tomato Mosaic Virus",
    "Tomato mosaic virus (ToMV) is a highly infectious plant virus that affects tomatoes and other members of the Solanaceae family. It is spread primarily through direct contact between infected and healthy plants, and also by mechanical transmission through contaminated tools, clothing, and equipment.",
    "Tomato mosaic virus (ToMV) resistance refers to the ability of tomato plants to resist infection by the ToMV virus. Resistance can be innate, meaning that the plant has natural mechanisms to prevent or limit the spread of the virus, or it can be acquired through breeding or genetic engineering.",
    "There are no chemicals that can effectively control tomato mosaic virus (ToMV) once a plant is infected. The best approach is to prevent the virus from infecting plants in the first place through the use of disease-free seeds, proper sanitation practices, and the control of insect vectors that can spread the virus.",
    "Sanitation refers to a set of practices aimed at preventing the spread of tomato mosaic virus (ToMV) in tomato plants. ToMV can be easily transmitted from plant to plant through contact with contaminated plant material, soil, tools, or clothing. Therefore, sanitation practices are crucial for preventing the virus from spreading."
]
Tomato_healthy = [
    'Tomato Healthy',
    "A healthy tomato culture would involve providing the plants with optimal growing conditions such as appropriate amounts of sunlight, water, nutrients, and spacing. This can involve selecting a suitable planting site with well-draining soil, ensuring adequate irrigation, fertilization, and pest management, and using good cultural practices such as pruning and trellising to improve air circulation and reduce the risk of diseases.",
    "Resistance in tomato plants refers to the ability of a particular variety or cultivar to withstand or tolerate certain pests, diseases, or environmental stresses, without suffering significant damage or yield losses. Resistance is often a desirable trait in tomato plants, as it can reduce the need for chemical inputs and improve overall plant health and productivity. Different tomato varieties may exhibit different levels of resistance to various pests and diseases, depending on their genetic makeup and growing conditions.",
    "Preventive measures such as using clean, disease-free seeds or transplants, rotating crops, providing proper nutrition and irrigation, and maintaining good hygiene practices in the garden can help promote plant health and reduce the risk of pest and disease infestations. In cases where chemical control is necessary for managing pests or diseases, it is important to choose products that are appropriate for the specific pest or disease, and to follow label instructions carefully to ensure safe and effective use.",
    "Tomato healthy sanitation practices refer to the measures taken to maintain a clean and hygienic environment for tomato plants. This involves removing any diseased plant materials or plant debris, including fallen leaves or fruits, from the growing area to prevent the spread of diseases. Sanitation practices also include cleaning and disinfecting garden tools, pots, and other equipment that come into contact with the plants to reduce the risk of spreading disease. Additionally, maintaining proper spacing between plants, providing adequate water and nutrients, and controlling pests can help promote plant health and prevent the spread of diseases. Overall, good sanitation practices can help prevent the development and spread of diseases that can harm tomato plants and reduce crop yields."
]

model = None

def download_blob(bucket_name, soucre_blob_name, destination_file_name):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(soucre_blob_name)
    blob.download_to_filename(destination_file_name)

app = Flask(__name__)


@app.route('/predict',methods=['POST','OPTIONS'])
def predict(request):
    global model
    if model is None:
        download_blob(
            BUCKET_NAME,
            "models/model1.h5",
            "/tmp/model1.h5",
        )
        model = tf.keras.models.load_model("/tmp/model1.h5")

    if request.method == 'OPTIONS':
        response = jsonify({'message': 'Success'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', '*')
        return response

    image = request.files["file"]

    image = np.array(Image.open(image).convert("RGB").resize((256,256)))
    image = image/255
    img_array = tf.expand_dims(image, 0)

    predictions = model.predict(img_array)

    idx = np.argmax(predictions[0])
    predicted_class = class_names[np.argmax(predictions[0])]
    confidence = round(100 * (np.max(predictions[0])), 2)

    classnames_arr = [Pepper__bell___Bacterial_spot,Pepper__bell___healthy,Potato___Early_blight,Potato___Late_blight,Potato___healthy,Tomato_Bacterial_spot,Tomato_Early_blight,Tomato_Late_blight,Tomato_Leaf_Mold,Tomato_Septoria_leaf_spot,Tomato_Spider_mites_Two_spotted_spider_mite,Tomato__Target_Spot,Tomato__Tomato_YellowLeaf__Curl_Virus,Tomato__Tomato_mosaic_virus,Tomato_healthy]


    # , "culture":classnames_arr[idx][1],"resistance":classnames_arr[idx][3],"chemicalcontrol":classnames_arr[idx][4],"sanitation":classnames_arr[idx][2]
    response = jsonify({"class": classnames_arr[idx][0], "confidence": confidence, "culture":classnames_arr[idx][1],"resistance":classnames_arr[idx][3],"chemicalcontrol":classnames_arr[idx][4],"sanitation":classnames_arr[idx][2]})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
