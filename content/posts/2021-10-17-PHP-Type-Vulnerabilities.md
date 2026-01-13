+++
title = "Untitled"
date = "2021-10-17T00:00:00+13:00"
draft = false
+++

# 

---

---

---

As with all good identification of poor application security, the devil is in the details (unless of course the
    security issues derives from poor design or logic, which in that case the devil is already there to stay and there
    is little you can do except burn the application). Without digressing too much however, we will look at an
    interesting but potentially costly vulnerability in PHP development commonly seen where equals comparisons are used
    instead of the more appropriate strict comparison, to which a PHP variable type juggling vulnerability can propogate
    leading to potential login bypass and breaking logic of search and comparison functions that exist in the
    application being examined.

In PHP, there are two main comparison modes:

- Equal PHP comparison: ==
- Identical PHP comparison: ===
According to PHP documentation, the Equal operator allows for checking if two values are equal after type juggling,
    whereas the identical comparison operator checks they are of the same type, regardless of type juggling. This is
    referred to strict vs loose comparisons.

![](/images/comparison_operator_type_info.png)

PHP does not require explicit type definition. Similar to var in JavaScript it is determined by the context of the
    variables it is storing and using (e.g., $foo = 1 is an integer variable, while $foo = "1" is a string variable).

Because of type juggling and loose comparisons, it is possible to trick an auth check or other comparison into
    doing something with a weird comparison juggling trick. The following example wile help to understand this concept.

Example:

Let's look at the following auth code:

`if($_GET['login']=="1"){
      // Note: An Equal strcmp() will return 0
      if(strcmp($_POST['user'], "admin") == 0 && strcmp($_POST['password'], "quantumbucks") == 0){
      echo "Welcome hacker";
      }else{
      echo "lol no";
      }`

It looks okay, until you realise that how this is taking in the password and username we send in the request, If we
    look at the table below, we should note that if we modified the request password="" in Burp Suite to password[]="".
    We then send in this array to compare against a string, strcmp() throws a null, and loosely compared to the 0 ends
    up being True and letting up in. This comparison has been highlighted in the table.

![](/images/comparison_operator_type_table.png)

Example Fix:

Let's rewrite this code:

`if($_GET['login']=="1"){
      // Note: An Equal strcmp() will return 0
      if(strcmp($_POST['user'], "admin") === 0 && strcmp($_POST['password'], "quantumbucks") === 0){
      echo "Welcome hacker";
      }else{
      echo "lol no";
      }`

As you can see here, using strict comparison operators would prevent the list being passed in. The strcmp()
    function would return NULL, and when compared to the 0 would show as... False.

![](/images/comparison_operator_type_table2.png)

The following type juggling example only talks to breaking strcmp() and utilising this create a bypass. More
    creative methods could also be implemented, especially where functions have been made by developers.

Resources:

[https://www.php.net/manual/en/types.comparisons.php](https://www.php.net/manual/en/types.comparisons.php)

[https://owasp.org/www-pdf-archive/PHPMagicTricks-TypeJuggling.pdf](https://owasp.org/www-pdf-archive/PHPMagicTricks-TypeJuggling.pdf)

[https://www.php.net/manual/en/language.operators.comparison.php](https://www.php.net/manual/en/language.operators.comparison.php)

[https://www.php.net/manual/en/language.types.type-juggling.php](https://www.php.net/manual/en/language.types.type-juggling.php)

---