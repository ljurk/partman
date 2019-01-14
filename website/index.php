<?php
include('func.php');
printHeader('Welcome to the future?!?!');
printNav();
?>

<ul>

<?php
function printInputs($categories) {
    $output = '<form action="action.php" method="post">
        <tr>
        <td>
        <input type="submit" value="speichern">
        </td>
        <td>';
    $output .= '<select name="categoryId" id="categoryId" size="';
    //$output .= (count($categories)) . '" >';
    $output .= '1">';
    $output .= jsonToSelect($categories);
    $output .= '</select>';
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
$json = file_get_contents('http://partapi/parts');
$obj = json_decode($json);
$json = file_get_contents('http://partapi/categories');
$categories = json_decode($json);

$parts = $obj->parts;
echo '<table class="json-table" width="100%">';
echo jsonToTableHeader($parts);
echo jsonToTable($parts);
echo printInputs($categories->categories);
echo '</table>'
?>

</ul>
</body>
</html>
