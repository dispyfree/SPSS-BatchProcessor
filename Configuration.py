import json
from Lang import Lang

class Configuration:
    currentVersion = 0.8;
    opt = {'inputSearchPattern': '', 'inputRegexPattern': '', 'outputFilePattern': '', 'outputDir': '',
           'placeholders': '', 'spssFile': '', 'defaultConfigDir': '', 'defaultSPSSDir': '', 'defaultInputDir': '',
           'defaultOutDir': '', 'programVersion': currentVersion, 'simulateProcessing': False,
           'inputFiles' : [], 'accumulateData' : False, 'accumulationFilePattern' : '', 'defaultSyntaxOutDir' : ''};
    reservedPlaceholders = opt.keys();

    """
    Filters files by the given pattern; is offered as a pattern when manually selecting files
    Example: *_averagedTrials.txt   will only show files ending with "_averagedTrials.txt"
    Example: *_Block*_trial.txt     will match files [subject]_Block[number]_trial.txt
    Please note that those patterns are _not_ full-fledged REGEX patterns, i.e. you should only use
    the wildcard "*" (matching anything) and fixed strings
    """
    opt['inputSearchPattern'] = '.txt';

    """
    Decomposes input file names into their  components, which can then be reused for the output files
    Example: (?P<fileName>[\w])*.txt                             parses files like "subject123_abc.txt" and assigns 
    "subject123_abc" to group "fileName" 
    Example: (?P<subject>[\w])*_Block(?P<blockNum>[\w])*.txt     parses files like "subject123_Block3.txt" and assigns 
        "subject123" to group "subject" as well as "3" to group "blockNum"
    The groups are provided as placeholders for use in input files: each occurance of "<groupName>" will be replaced 
    in the input files. 

    These are indeed full-fledged REGEX expressions. The captured groups ("capture groups") can be reused in 
    outputFilePattern.
    @see https://docs.python.org/2/howto/regex.html#grouping
    """
    opt['inputRegexPattern'] = '(?P<fileName>[\w]*).txt';

    """
    Specifies the output file to use for SPSS. The output file name will be available as "<OUTPUTFILE>" in the spss 
    syntax.   Group names captured in the inputRegexPattern may be used to compose the output file name.
    Please note that there is no need to actually use <OUTPUTFILE> in the syntax - in this case, just specify a dummy
    for this placeholder.

    Example: <fileName>.sav     if inputRegexPattern is "(?P<fileName>[\w])*.txt", this will simply change the 
    extension when saving the result file
    Example: <subject>_someFancyProcessingStep_Block<blockNum>.sav  if inputRegexPattern is defined as in the second 
    example above, this will yield an output file name such as "subject123_someFancyProcessingStep_Block3.sav"
    """
    opt['outputFilePattern'] = '';

    """
    Output directory; please use relative path names 
    """
    opt['outputDir'] = './output';

    """
    Defines placeholders and their value to be substituted for them in the input files
    INFILE and OUTFILE are always determined automatically, taking self.opt.inputRegexPattern, 
    self.opt.outputFilePattern into account. Thus, they cannot be set manually. 
    """
    opt['placeholders'] = {'INFILE': '', 'OUTPUTFILE': '', 'DUMMY': 'DUMMY'};

    opt['spssFile'] = 'none selected';
    opt['inputFiles'] = [];

    """
    Defaults change to whatever the user chose last; this speeds up work considerably as we do not have to navigate
    to the right places over and over again
    """
    opt['defaultConfigDir'] = '.';
    opt['defaultSPSSDir'] = '.';
    opt['defaultInputDir'] = '.';
    opt['defaultOutDir'] = '.';

    # by default do NOT simulate
    opt['simulateProcessing'] = False;

    """
    Data accumulation is a special function which merges the cases of all selected files into one target file
    By default, this special function is disabled. Enabling it enforces execution of 
    @see accumulationFileTemplate
    """
    opt['accumulateData'] = False


    """
    Pattern used to accumulate files; overwrites any value specified by the user
    For accumulation, there is no need to extract information from the file name; therefore a standard pattern
    is indeed sufficient.
    """
    opt['accumulationFilePattern'] = '(?P<fileName>[\w]*).sav'


    """
    The very last file from the input files is selected, copied into the destination directory and renamed 
    as defined in the following. Please note that the syntax in
    @accumulationFileTemplate
    has to be adapted whenever this value is changed. 
    """
    accumulationFileName ='accumulate.sav'

    """
    Defines the directory to use for writing out transient SPSS syntax. 
    If not 'none' but a real directory, for each input file "fileName.ext", a corresponding syntax file "fileName.sps" 
    will be generated
    """
    opt['defaultSyntaxOutDir'] = 'none'


    """
    Template for merging/accumulating data files
    """
    accumulationFileTemplate = 'C:/Users/admin/Documents/valentin/BatchProcessor/workflow/Schritt_2_Zusammenfügen_der_SavDateien.sps'

    def getCurrentVersion(self):
        return self.currentVersion;

    def loadFromString(self, str):
        self.opt = json.loads(str);

    def loadFromFile(self, f):
        self.opt = json.load(f);
        # check config file version
        if (self.opt['programVersion'] > self.getCurrentVersion()):
            BatchProcessor.err(Lang.get("The config file was created using a newer program version. Settings might be ignored and behavior may change. To avoid surprises, please updated the BatchProcessor."))

    def toJSON(self):
        return json.dumps(self.opt, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def ObjToJSON(self, obj):
        return json.dumps(obj, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
