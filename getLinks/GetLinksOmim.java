import java.io.IOException;

public class GetLinksOmim {
	
	public static void main(String[] args) throws IOException {
		
		String resourceName = "omim";
		String ftpLinks = "ftp://ftp.ncbi.nih.gov/repository/OMIM/ARCHIVE/omim.txt.Z\n";
		
		new GetBulkLinks(resourceName,ftpLinks);

	}

}
