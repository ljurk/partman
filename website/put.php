<?php
include('func.php');
$referer = strtok($_SERVER['HTTP_REFERER'], '?');
echo $referer;
if(endsWith($referer,"/categories.php") == true){
    $service_url = 'http://pm-api:3000/categories';
    $curl_post_data = array(
        'name' => $_POST['name']
);
    echo $_POST['name'];
}else{
    $service_url = 'http://pm-api:3000/parts';
    $curl_post_data = array(
        'categoryId' => (int)$_POST['categoryId'],
        'name' => $_POST['name'],
        'friendlyName' => $_POST['friendlyName'],
        'amount' => (int)$_POST['amount']
);
    echo $_POST['categoryId'];
}
echo $service_url;
$curl = curl_init($service_url);
curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
curl_setopt($curl, CURLOPT_CUSTOMREQUEST, "PUT");
curl_setopt($curl, CURLOPT_POSTFIELDS, $curl_post_data);
$curl_response = curl_exec($curl);
if ($curl_response === false) {
    $info = curl_getinfo($curl);
    curl_close($curl);
    die('error occured during curl exec. Additioanl info: ' . var_export($info));
}
curl_close($curl);
$decoded = json_decode($curl_response);
if (isset($decoded->response->status) && $decoded->response->status == 'ERROR') {
    die('error occured: ' . $decoded->response->errormessage);
}
echo 'response ok!';
var_export($decoded->response);
?>

<meta http-equiv="refresh" content="0; URL='<?php echo $referer . '?status=success';?>'" />
