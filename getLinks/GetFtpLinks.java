import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;


public class GetFtpLinks {

	final String ROOT = "../../";
	
	public GetFtpLinks(String resourceName, String ftpLinks) throws IOException{
		FileWriter fstream = new FileWriter(ROOT+"links/"+"ftpLinks."+resourceName+".txt");
		BufferedWriter out = new BufferedWriter(fstream);
		out.append(ftpLinks);
		out.close();
	}

	public static void main(String[] args) {
	}

}
