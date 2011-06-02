import java.io.IOException;

public class GetLinksMedline {
	public static void main(String[] args) throws IOException {
		
		String resourceName = "medline";
		String ftpLinks = "ftp://ftp.nlm.nih.gov/nlmdata/.medleasebaseline/zip/*.zip\n";
		
		new GetBulkLinks(resourceName,ftpLinks);

	}
}
