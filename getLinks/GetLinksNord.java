import java.io.IOException;
import java.util.List;

import com.gargoylesoftware.htmlunit.html.HtmlElement;
import com.gargoylesoftware.htmlunit.html.HtmlPage;


public class GetLinksNord {
	public static void main(String[] args) throws IOException
	{
		GetWebLinks gl = new GetWebLinks();
		
		for(int i=1;i<=1201;i=i+100)
			gl.alphabetLinks.add("http://rarediseases.org/search/rdblist.html?query_start="+i);

		for(String link: gl.alphabetLinks){
			HtmlPage currentPage = gl.webClient.getPage(link);
			List<HtmlElement> spans = currentPage.getBody().getElementsByAttribute("span","class","feature_body");
			for(HtmlElement span: spans){
				//System.out.println(span.asXml());
				if(span.getChildNodes().getLength() > 1)
					try{
						HtmlElement anchor = span.getElementsByTagName("a").get(0);
						String href = anchor.getAttribute("href");
						if(! href.startsWith("http://rarediseases.org/search/rdblist.html?query_start=") && ! href.equals("/search/rdbdetail_abstract.html?disname="))
							gl.articleLinks.add("http://rarediseases.org"+anchor.getAttribute("href"));
					}catch(Exception e){
						e.printStackTrace();
					}

			}
			
		}
		gl.removeDuplicateLinks();
		gl.writeLinksToFile("nord");
	}
}
