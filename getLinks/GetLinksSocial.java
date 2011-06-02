import java.io.IOException;
import java.util.List;

import com.gargoylesoftware.htmlunit.html.HtmlElement;


public class GetLinksSocial {
	public static void main(String[] args) throws IOException
	{
		GetWebLinks gl = new GetWebLinks("http://www.socialstyrelsen.se/rarediseases");
		
		HtmlElement pageBody = gl.currentPage.getHtmlElementById("socextContentPageArea");
		HtmlElement tableBody = (HtmlElement) pageBody.getByXPath("table/tbody").get(0);
		
		List<HtmlElement> anchors = tableBody.getElementsByTagName("a");
		for(HtmlElement anchor: anchors)
			gl.articleLinks.add(anchor.getAttribute("href"));
		
		gl.removeDuplicateLinks();
		gl.writeLinksToFile("social");
	}
}
