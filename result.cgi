#!/usr/bin/env ruby

require "cgi"
require "open-uri"
require "json"
cgi = CGI.new

puts cgi.header("text/html; charset=UTF-8")
print("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.01 Frameset//EN\" \"http://www.w3.org/TR/html4/frameset.dtd\">")
print("<html>")
print(" <head>")
print("  <title>検索結果</title>")
print("  <link rel=\"stylesheet\" type=\"text/css\" href=\"style.css\">")
print(" </head>")
print("<body>")
print("<center>")
print(" <a href=\"search.html\"><font id=\"title\">Solr</font>&nbsp; &nbsp; Wikipedea:気候</a>")
print("
    <form id=\"search\" style=\"display: inline\" method=\"GET\" action=\"result.cgi\" >
   <input type=\"text\" size=\"25\" name=\"q\">
   <input type=\"hidden\" name=\"page\" value=1>
   <input id=\"bo\" type=\"submit\" value=\"検索\">
  </form>
 <br>
 <hr>
 <hr id=\"sen1\">")
print("<font color=\"blue\">検索結果</font><br><br>")

if cgi["q"] == "" or cgi["q"] == " " or cgi["q"] == "　"
	print("文字を入力してください！<br>")
else
  page =cgi["page"].to_i
  start_p = (page - 1)*10
  io = open("http://localhost:8983/solr/wikipedia/select?q=#{URI.escape cgi["q"]}&rows=10&start=#{start_p}&wt=json")
  json = io.read
  data = JSON.load(json)
  result_sum = data["response"]["numFound"]

#検索結果表示
  if result_sum == 0
    print("\" #{cgi["q"]} \"<br>")
	  print("該当するものはありませんでした<br>")
  else
      print("\" #{cgi["q"]} \"<br>")
      print("#{result_sum}件<br><br>")
      result = data["response"]["docs"]

#結果表示
   print("<table align=\"center\">")
   i = start_p + 1
   result.each do |e|
      print("<tr>")
      print("<td width = \"60\" align=\"center\" height= \"40\">#{i}</td>")
      puts("<td>",e["title"],"</td>")
      print("<tr>")
	  i = i + 1
    end
      print("</table>")
      print("<br>")

    #ページ
    print("<table id=\"page\">")
    print("<tr>")
    if page != 1
      print("<td id=\"push\"><a href=\"result.cgi?q=#{cgi["q"]}&page=", page-1 ,"\">", page-1, "</a></td>")
    end
    print("<td id=\"now\">",cgi["page"],"</td>")
    if page < (result_sum.to_f/10)
     print("<td id=\"push\"><a href=\"result.cgi?q=#{cgi["q"]}&page=",page+1,"\">", page+1, "</a></td>")
    end
    print("</tr>")
    print("</table>")
   end
end
print("</center>")
print("</body>")
print("</html>")