<html>
    <head>
        <title>partman</title>
        <!--<style>
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
        </style>-->
		<link rel="stylesheet" href="style.css">
    </head>
    <body>
        <h1>Welcome to the future</h1>
        <nav id="TOC">
	    <ul>
	        <li>
		    <a href="categories.php">categories</a>
		</li>
                <li>
                    <?php
                        if($_GET['status'] == 'success'){
                            $uri = explode('?', $_SERVER['REQUEST_URI'], 2);
                            $host = "http://$_SERVER[HTTP_HOST]$uri_paths";
                            echo '<meta http-equiv="refresh" content="1; URL=' . $host . '"/>';
                            echo '<a href=""> <font color="#68cc6d" >success</font></a>';
                        }
                    ?>
                </li>
            </ul>
        </nav>
        <ul>
            <?php
                function printHeader() {
                    $table ='<tr>
                        <td>id</td>
                        <td>category</td>
                        <td>name</td>
                        <td>friendlyName</td>
                        <td>amount</td>
                        </tr>';
                    return $table;
                }
                function jsonToSelect ($data) {
                    foreach ($data as $key => $value) {
                        if (is_object($value) || is_array($value)) {
                            //$outputSelect .= jsonToSelect($value);
                            $key = $key + 1;
                            $outputSelect .= '<option value='. $key .' >' . $value->name . '</option>';
                        }
                    }
                    return $outputSelect;
                }

                function jsonToTable ($data) {
                    $table .= '<tr>';
                    foreach ($data as $key => $value) {
                        if (is_object($value) || is_array($value)) {
                            $table .= '</tr>';
                            $table .= jsonToTable($value);
                        } else {
                            $table .= '<td>';
                            if($key=='id'){
                                $table .= '<form action="delete.php" method="post"><button type="submit" value="'.$value.'" name="id">X</button>'.$value.'</form>';
                            } else {
                                $table .= $value;
                            }
                            $table .= '</td>';
                        }
                    }
                    return $table;
                }
                function printInputs($categories){
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
                echo printHeader();
                echo jsonToTable($parts);
                echo printInputs($categories->categories);
                echo '</table>'
            ?>
        </ul>
    </body>
</html>
