import React from 'react';

const TablePest = () => {
  return (
    <>
    <center><h1 style={{backgroundColor: "#f2f2f2"}}>Treatment Information</h1></center>
    <table style={{backgroundColor: "#f2f2f2",borderCollapse: "collapse", width: "100%"}}>
      <thead style={{backgroundColor: "#f2f2f2"}}>
        <tr>
          <th style={{border: "1px solid black", padding: "8px"}}>Information Name</th>
          <th style={{border: "1px solid black", padding: "8px"}}>Details</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td style={{border: "1px solid black", padding: "8px"}}>Disease Type</td>
          <td style={{border: "1px solid black", padding: "8px"}}>Tomato Leaf Mold</td>
        </tr>
        <tr>
          <td style={{border: "1px solid black", padding: "8px"}}>Culture</td>
          <td style={{border: "1px solid black", padding: "8px"}}>The cultural practices for reducing the disease. It includes adequating row and plant spacing that promote better air circulation through the canopy reducing the humidity; preventing excessive nitrogen on fertilization since nitrogen out of balance enhances foliage disease development; keeping the relatively humidity below 85% (suitable on greenhouse), promote air circulation inside the greenhouse, early planting might to reduce the disease severity and seed treatment with hot water (25 minutes at 122 °F or 50 °C)</td>
        </tr>
        <tr>
          <td style={{border: "1px solid black", padding: "8px"}}>Sanitation</td>
          <td style={{border: "1px solid black", padding: "8px"}}>The sanitization control in order to reduce the primary inoculum. Remove and destroy (burn) all plants debris after the harvest, scout for disease and rogue infected plants as soon as detected and steam sanitization the greenhouse between crops.</td>
        </tr>
        <tr>
          <td style={{border: "1px solid black", padding: "8px"}}>Resistance</td>
          <td style={{border: "1px solid black", padding: "8px"}}>The most effective and widespread method of disease control is to use resistant cultivars. However, only few resistant cultivar to tomato leaf mold are known such as Caruso, Capello, Cobra (race 5), Jumbo and Dombito (races 1 and 2). Moreover, this disease is not considered an important disease for breeding field tomatoes</td>
        </tr>
        <tr>
          <td style={{border: "1px solid black", padding: "8px"}}>Chemical Control</td>
          <td style={{border: "1px solid black", padding: "8px"}}>The least but not the less important management is the chemical control that ensure good control of the disease. The chemical control is basically spraying fungicide as soon as the symptoms are evident. Compounds registered for using are: chlorothalonil, maneb, mancozeb and copper</td>
        </tr>
      </tbody>
    </table>
    </>
  );
};

export default TablePest;
