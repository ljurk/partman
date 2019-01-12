<html>
    <head>
        <title>My Shop</title>
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
        <h1>Welcome to my shop</h1>
        <ul>
            <?php
                function printHeader()
                {
                    $table ='<tr><td>id</td><td>name</td><td>category</td><td>friendlyName</td></tr>';
                    return $table;
                }
                function jsonToTable ($data)
                {
//                    if(!is_array($data)) {
                        $table .= '<tr>';
 //                   }
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
            $json = file_get_contents('http://partapi/');
            $obj = json_decode($json);


            $parts = $obj->parts;
            echo '<table class="json-table" width="100%">';
            echo printHeader();
            echo jsonToTable($parts);
            echo '</table>' 

      //      foreach ($parts as $part) {
      //          echo "<li>$part</li>";
       //     }

            ?>
        </ul>
    </body>
</html>
