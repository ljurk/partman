<html>
    <head>
        <title>partman</title>
        <style>
            table {
                font-family: arial, sans-serif;
                border-collapse: collapse;
                width: 100%;
            }
            td, th {
                border: 1px solid #dddddd;
                text-align: left;
                padding: 8px;
            }
            tr:nth-child(even) {
                background-color: #dddddd;
            }
        </style>
    </head>
    <body>
        <h1>Categories</h1>
        <a href="index.php">parts</a> 
        <ul>
            <?php
                function printHeader() {
                    $table ='<tr><td>id</td><td>name</td></tr>';
                    return $table;
                }
                function jsonToTable ($data) {
                    $table .= '<tr>';
                    foreach ($data as $key => $value) {
                        if (is_object($value) || is_array($value)) {
                            $table .= '</tr>';
                            $table .= jsonToTable($value);
                        } else {
                            $table .= '<td>';
                            $table .= $value;
                            $table .= '</td>';
                        }
                    }
                    return $table;
                }
                function printInputs(){
                    $output = '<form action="action.php" method="post">
                            <tr>
                            <td>
                            <input type="submit" value="speichern">
                            </td>
                            <td>
                            <input type="text" name="name" id="name">';

                    if($_GET['status'] == 'success'){
                       $output .= '<font color="green" size="5"><b>success</b></font>';
                    }
                            $outpu .='</td>
                            </tr>
                        </form>';
                    return $output;
                }
                $json = file_get_contents('http://partapi/categories');
                $obj = json_decode($json);


                $parts = $obj->categories;
                echo '<table class="json-table" width="100%">';
                echo printHeader();
                echo jsonToTable($parts);
                echo printInputs();
                echo '</table>'
            ?>
        </ul>
    </body>
</html>
