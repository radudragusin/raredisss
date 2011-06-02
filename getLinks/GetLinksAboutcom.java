import java.io.IOException;
import java.util.List;
import java.util.concurrent.CopyOnWriteArrayList;

import com.gargoylesoftware.htmlunit.ElementNotFoundException;
import com.gargoylesoftware.htmlunit.html.HtmlElement;


public class GetLinksAboutcom {
	public static void main(String[] args) throws IOException
	{
		GetWebLinks gl = new GetWebLinks("http://rarediseases.about.com/od/rarediseasesad/Information_About_Rare_Diseases_A_B.htm");
		gl.alphabetLinks = new CopyOnWriteArrayList<String>();
		
		// Create a list of links that point to alphabetical categories of rare diseases lists 
		HtmlElement listing = gl.currentPage.getElementById("sub");
		List<HtmlElement> listElements = (List<HtmlElement>) listing.getElementsByTagName("a");
		for(HtmlElement row: listElements)
			gl.alphabetLinks.add(row.getAttribute("href"));

		// Add new links pointing to rare diseases lists
		for(String link: gl.alphabetLinks) {
			gl.currentPage = gl.webClient.getPage("http://rarediseases.about.com"+link);
			HtmlElement body = gl.currentPage.getElementById("articlebody");

			try{
				HtmlElement sublist = body.getElementById("sub");
				List<HtmlElement> sublistElements = (List<HtmlElement>) sublist.getElementsByTagName("a");
				for(HtmlElement element: sublistElements)
					gl.alphabetLinks.add(element.getAttribute("href"));
			} catch (ElementNotFoundException e) {}
		}
		
		// Store all article links
		for(String link: gl.alphabetLinks) {
			gl.currentPage = gl.webClient.getPage("http://rarediseases.about.com"+link);
			HtmlElement body =gl.currentPage.getElementById("articlebody");
			
			List<HtmlElement> divs = body.getHtmlElementsByTagName("div");
			for(HtmlElement div: divs){
				// Get links of disease articles
				if(div.getAttribute("id").matches("^l\\d+$")){
					HtmlElement anchor = (HtmlElement) div.getByXPath("h2/a").get(0);
					String href = anchor.getAttribute("href");
					if(!href.contains("http://"))
						gl.articleLinks.add("http://rarediseases.about.com"+href);
				}
			}
		}
		
		gl.removeDuplicateLinks();
		gl.writeLinksToFile("aboutcom");
	}
}
