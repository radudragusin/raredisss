import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.Date;
import java.text.SimpleDateFormat;

import com.gargoylesoftware.htmlunit.WebClient;
import com.gargoylesoftware.htmlunit.html.HtmlPage;


public class GetWebLinks {
	
	final String ROOT = "../../"; //"/Users/paula/master/";
	protected List<String> alphabetLinks;
	protected List<String> articleLinks;
	protected WebClient webClient;
	protected HtmlPage currentPage;
	protected String[] result;
	protected long startTime;
	
	public GetWebLinks(String startPage){
		alphabetLinks = new ArrayList<String>();
		articleLinks = new ArrayList<String>();
				
		webClient = new WebClient();
		webClient.setJavaScriptEnabled(false);
		
		startTime = System.nanoTime();
		try{
			currentPage = webClient.getPage(startPage);
		}catch(Exception e) {
			e.printStackTrace();
		}
	}
	public GetWebLinks(){
		alphabetLinks = new ArrayList<String>();
		articleLinks = new ArrayList<String>();
				
		webClient = new WebClient();
		webClient.setJavaScriptEnabled(false);
		
		startTime = System.nanoTime();
	}
	
	public void removeDuplicateLinks(){
		Set<String> set = new HashSet<String>(articleLinks);
		result = new String[set.size()];
		set.toArray(result);
	}
	
	public void writeLinksToFile(String resourceName) throws IOException{
//		System.out.println("Number of alphabet links: "+alphabetLinks.size());
//		FileWriter fstream1 = new FileWriter("alphabetLinks."+resourceName+".txt");
//		BufferedWriter out1 = new BufferedWriter(fstream1);
//		for(String link: alphabetLinks)
//			out1.append(link+"\n");
//		out1.close();

		
		long elapsedTime = System.nanoTime() - startTime;
		double seconds = (double)elapsedTime / 1000000000.0;
		SimpleDateFormat sdf = new SimpleDateFormat("MM/dd/yyyy hh:mm:ss a");
		Date date = new Date();
		
		FileWriter fstream = new FileWriter(ROOT+"links/"+"webLinks."+resourceName+".txt");
		BufferedWriter out = new BufferedWriter(fstream);
		for(String link: result)
			out.append(link+"\n");
		out.close();
		
		System.out.println("Finished getting links for resource: "+resourceName);
		System.out.println("--Number of links: "+articleLinks.size());
		System.out.println("--Number of unique links: "+result.length);
		System.out.println("--Extracted all links in: "+seconds+" sec");
		System.out.println("--"+sdf.format(date));

		fstream = new FileWriter(ROOT+"links/"+"webLinks."+resourceName+".stat");
		out = new BufferedWriter(fstream);
		out.append("Number of links: "+articleLinks.size()+"\n");
		out.append("Number of unique links: "+result.length+"\n");
		out.append("Extracted all links in: "+seconds+" sec\n");
		out.append(sdf.format(date));
		out.close();
		
	}
	
	public static void main(String[] args) {
	}

}
