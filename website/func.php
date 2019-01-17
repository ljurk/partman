<?php
function endsWith($string, $endString)
{
        $len = strlen($endString);
            if ($len == 0) {
                        return true;
                            }
    return (substr($string, -$len) === $endString);
}

function printHeader($h1) {
    echo '<html>
        <head>
        <title>partman</title>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js"></script>
<script src="scripts/jq.js"></script>
        <link rel="stylesheet" href="style.css">
        </head>
        <body>
        <h1>'.$h1.'</h1>';
}

function printNav() {
    echo '<nav id="TOC">
        <ul>
        <li>
        <a href="'.$GLOBALS["subfolder"].'/">parts</a>
        </li>
        <li>
        <a href="'.$GLOBALS["subfolder"].'/categories.php">categories</a>
        </li>
        <li>
        <a href="'.$GLOBALS["subfolder"].'/api">api</a>
        </li>
        <li>';
    if($_GET['status'] == 'success') {
        printSuccess();
    }
    echo '</li>
        </ul>
        </nav>';
}

function printSuccess() {
    $uri = explode('?', $_SERVER['REQUEST_URI'], 2);
    $host = "http://$_SERVER[HTTP_HOST]".$GLOBALS['subfolder'].$uri[0];
    echo '<meta http-equiv="refresh" content="1; URL=' . $host . '"/>';
    echo '<a href=""> <font color="#68cc6d" >success</font></a>';
}

function jsonToTableHeader ($data) {
    if(sizeof($data)!=0){
        $outputSelect = '<tr>';
        $row = $data[0];
        foreach($row as $key => $val) {
            echo '<td>';
            echo $key ;
            echo '</td>';
        }
    }
    $outputSelect .= '</tr>';
    return $outputSelect;
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
            if($key=='id') {
                $table .= '<form action="' . $GLOBALS["subfolder"] . '/delete.php" method="post"><button type="submit" value="'.$value.'" name="id">X</button>'.$value.'</form>';

            }elseif($key=='amount') {
                $table .= '<form action="' . $GLOBALS["subfolder"] . '/update.php" method="post"><input type="number" name="amount" id="amount" min="0" value="'.$value.'"><button type ="submit" />change</form>';

            }elseif($key == 'name' || $key == 'description'){
                $table .= '<span id="'.$GLOBALS['contentid'].'"contenteditable="true">'
                    .$value.
                    '</span>';
                $GLOBALS['contentid'] =$GLOBALS['contentid'] + 1;
            } else {
                $table .= $value;
            }
            $table .= '</td>';
        }
    }
    return $table;
}
?>
