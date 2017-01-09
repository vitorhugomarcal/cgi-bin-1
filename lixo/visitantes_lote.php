<!DOCTYPE html>
<title>Cadastro de Visitantes em Lote</title>
<head>

<style>
body
{
background-color: #575757;
color: #f5f1e9;
font-family: 'Roboto', sans-serif;
}

div
{
-webkit-box-shadow: 3px 3px 15px 0px rgba(0,0,0,0.75);
-moz-box-shadow: 3px 3px 15px 0px rgba(0,0,0,0.75);
box-shadow: 3px 3px 15px 0px rgba(0,0,0,0.75);

background-color: #2c4d9c;
font-size: 35px;
padding: 25px;
text-align: center;
width: 60%;
border: 2px solid #152343;
border-radius: 10px;
color: white;
}

.input_campos
{
background-color: #1f2d4a;
color: #575757;
border: 2px solid #152343;
border-radius: 5px;
color: white;
padding: 5px;
width: 60%;
}

input
{
background-color: #1f2d4a;
color: #575757;
border: 2px solid #152343;
border-radius: 5px;
color: white;
padding: 5px;
}


</style>
</head>

<body>
<br><br>
<center>
<div>
</br>
Cadastro de Visitantes em Lote</br></br>
<form action="/cgi-bin/cadastra_visitante_lote.py" method="POST">
<input class="input_campos" type="text" name="crachaini" placeholder="Digite o numero do Crachá Inicial"></br>
<input class="input_campos" type="text" name="crachafim" placeholder="Digite o numero do Crachá Final"></br>

<select name="crachaativo">
<option value="A">Ativar Todos</option>
</select>

</br>
<input type="submit" value=" Gravar ">
<br><br>
</form>
</div>
</center>
</body>
</html>
