import java.io.IOException;
import java.util.List;

import com.gargoylesoftware.htmlunit.html.HtmlElement;


public class GetLinksHon {
	public static void main(String[] args) throws IOException
	{
		GetWebLinks gl = new GetWebLinks("http://www.hon.ch/HONselect/RareDiseases/index.html");
		
		HtmlElement table = gl.currentPage.getBody().getElementsByTagName("table").get(4);
		List<HtmlElement> anchors = table.getElementsByTagName("a");
		for(HtmlElement anchor: anchors){
			String href = anchor.getAttribute("href");
			href = href.replace("RareDiseases/", "RareDiseases/EN/");
			gl.articleLinks.add("http://www.hon.ch"+href);
		}
		
		gl.removeDuplicateLinks();
		gl.writeLinksToFile("hon");
	}
}
