import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;


public class GetBulkLinks {

	final String ROOT = "../../";
	
	public GetBulkLinks(String resourceName, String ftpLinks) throws IOException{
		FileWriter fstream = new FileWriter(ROOT+"links/"+"bulkLinks."+resourceName+".txt");
		BufferedWriter out = new BufferedWriter(fstream);
		out.append(ftpLinks);
		out.close();
		System.out.println("Finished getting links for resource: "+resourceName);
	}

	public static void main(String[] args) {
	}

}
