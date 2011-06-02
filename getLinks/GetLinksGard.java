import java.io.IOException;
import java.util.List;

import com.gargoylesoftware.htmlunit.html.HtmlElement;
import com.gargoylesoftware.htmlunit.html.HtmlForm;


public class GetLinksGard {

	public static void main(String[] args) throws IOException
	{
		
		GetWebLinks gl = new GetWebLinks("http://rarediseases.info.nih.gov/RareDiseaseList.aspx?PageID=1");
				
		HtmlElement table = gl.currentPage.getElementsByTagName("table").get(0);
		List<HtmlElement> anchors = table.getElementsByTagName("a");
		for(HtmlElement anchor: anchors)
			gl.alphabetLinks.add(anchor.getAttribute("href"));
		
		for(String link: gl.alphabetLinks){
			gl.currentPage = gl.webClient.getPage("http://rarediseases.info.nih.gov/"+link);
			HtmlForm form = gl.currentPage.getFormByName("Form1");
			HtmlElement list = (HtmlElement) form.getByXPath("div/div/div/div[3]/ul").get(0);
			List<HtmlElement> anchorsArticles = list.getElementsByTagName("a");
			for(HtmlElement anchor: anchorsArticles){
				gl.articleLinks.add("http://rarediseases.info.nih.gov/"+anchor.getAttribute("href"));
			}
		}
		
		gl.removeDuplicateLinks();
		gl.writeLinksToFile("gard");
	}

}
