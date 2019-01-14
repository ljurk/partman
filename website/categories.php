<?php
include('func.php');
printHeader('Categories');
printNav();
?>

<ul>

<?php
function printInputs() {
    $output = '<form action="action.php" method="post">
        <tr>
        <td>
        <input type="submit" value="speichern">
        </td>
        <td>
        <input type="text" name="name" id="name">
        </td>
        </tr>
        </form>';
    return $output;
}
$json = file_get_contents('http://partapi/categories');
$obj = json_decode($json);


$categories = $obj->categories;
echo '<table class="json-table" width="100%">';
echo jsonToTableHeader($categories);
echo jsonToTable($categories);
echo printInputs();
echo '</table>'
?>

</ul>
</body>
</html>
