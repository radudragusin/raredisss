import java.io.IOException;
import java.util.List;

import com.gargoylesoftware.htmlunit.html.HtmlElement;
import com.gargoylesoftware.htmlunit.html.HtmlPage;


public class GetLinksMadisons {
	public static void main(String[] args) throws IOException
	{
		GetWebLinks gl = new GetWebLinks();
		
		for(int i=1;i<=105;i++)
			gl.alphabetLinks.add("http://www.madisonsfoundation.org/index.php/component/option,com_mpower/Itemid,49/page,"+i+"/letter,All/");
		
		for(String link: gl.alphabetLinks){
			HtmlPage currentPage = gl.webClient.getPage(link);
			HtmlElement mainColumn = currentPage.getElementById("maincolumn");
			List<HtmlElement> divs = mainColumn.getElementsByTagName("div");
			for(HtmlElement div: divs){
				if (div.getAttribute("class").contentEquals("readmore")){
					HtmlElement anchor = div.getElementsByTagName("a").get(0);
					gl.articleLinks.add(anchor.getAttribute("href"));
				}
			}
		}
		
		gl.removeDuplicateLinks();
		gl.writeLinksToFile("madisons");
	}
}
