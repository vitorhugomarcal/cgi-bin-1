<!DOCTYPE html>
<title>Cadastro de Funcionarios</title>
<body>
<pre>
<center>
Cadastro de Funcionários</br>
<form action="/cgi-bin/cadastro_funcionarios.py" method="POST">
<input type="text" name="cracha" placeholder="Digite o numero do Crachá..."></br>
<input type="text" name="nome" placeholder="Digite o nome do Funcionário..."></br>

<?php
$con = new mysqli("127.0.0.1","root","161879","wfp") or die(mysql_error());
$qrylista = mysqli_query($con,"select * from controladora");

echo "Local de Acesso<br>";
echo "<select name='controladora'>";
echo "<option value='Todas'>Acesso Total</option>";
while($resultado = mysqli_fetch_assoc($qrylista)){

echo "<option value='".$resultado['ip']."'>".$resultado['nome']."</option>";

}
echo "</select>";


?>


<input type="submit" value=" Gravar ">
</form>
</center>
</pre>
</body>
</html>
