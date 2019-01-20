<?php
$GLOBALS["contentid"] = 1;
$GLOBALS["subfolder"] = '';
include('func.php');
printHeader('Welcome to the future?!?!');
printNav();
?>

<ul>

<?php
$url = 'http://partapi/parts';
$user = 'user';
$pw = 'password';
function printInputs($categories) {
    $output = '<form action="' . $GLOBALS["subfolder"] . '/put.php" method="post">
        <tr>
        <td>
        <input type="submit" value="speichern">
        </td>
        <td>';
    #$output .= '<select name="categoryId" id="categoryId" size="';
    #$output .= '1">';
    $output .= jsonToSelect($categories);
    #$output .= '</select>';
    $output .= '</td>
        <td>
        <input type="text" name="name" id="name">
        </td>
        <td>
        <input type="text" name="friendlyName" id="friendlyName">
        </td>
        <td>
        <input type="number" name="amount" id="amount" min="0">';

    $output .= '</td>
        </tr>
        </form>';
    return $output;
}
$context = stream_context_create(array (
    'http' => array (
        'header' => 'Authorization: Basic ' . base64_encode("$user:$pw")
    )
));
//$json = file_get_contents($url,false,$context);
$json = file_get_contents($url);
$obj = json_decode($json);
$json = file_get_contents('http://partapi/categories');
$categories = json_decode($json);

$parts = $obj->parts;
echo '<table class="json-table" width="100%">';
echo jsonToTableHeader($parts);
echo jsonToTable($parts, $categories->categories, 0);
echo printInputs($categories->categories);
echo '</table>'
?>

</ul>
</body>
</html>
