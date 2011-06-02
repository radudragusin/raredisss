import java.io.IOException;
import java.util.List;

import com.gargoylesoftware.htmlunit.html.HtmlElement;


public class GetLinksGhr {
	public static void main(String[] args) throws IOException
	{
		GetWebLinks gl = new GetWebLinks("http://ghr.nlm.nih.gov/BrowseConditions");
				
		HtmlElement div = gl.currentPage.getBody().getElementsByTagName("div").get(9);
		List<HtmlElement> anchors = div.getElementsByTagName("a");
		for(HtmlElement anchor: anchors){
			gl.alphabetLinks.add(anchor.getAttribute("href"));
		}

		for(String link: gl.alphabetLinks){
			gl.currentPage = gl.webClient.getPage(link);
			HtmlElement list = gl.currentPage.getElementsByTagName("ul").get(1);
			List<HtmlElement> anchorsArticles = list.getElementsByTagName("a");
			for(HtmlElement anchor: anchorsArticles){
				String href = anchor.getAttribute("href");
				if(! href.contains("conditionGroup"))
					gl.articleLinks.add(anchor.getAttribute("href"));
			}
		}
		
		gl.removeDuplicateLinks();
		gl.writeLinksToFile("ghr");
	}
}
