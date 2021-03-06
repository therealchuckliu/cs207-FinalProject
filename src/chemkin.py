import numbers
import xml.etree.ElementTree as ET
import numpy as np


class ElementaryReaction():
    """Class for a each elementary reaction.

    Take a dictionaries of properties from the XMLReader class. 
    Calculates the rate coefficient for each elementary reaction and returns it to
    the ReactionSystem class. Returns a dictionary of recatants and products 
    to the ReactionSystem class. Following methods are implemented in the class-
    
    __init__(self, reaction_properties)
    __repr__(self)
    get_reactants(self)
    get_products(self)
    calculate_rate_coefficient(self, T)
    """
    
    def __init__(self, reaction_properties):
        """
        Constructor for the class

        EXAMPLES:
        =========
        >>> elementary_reaction = ElementaryReaction({'equation' : 'H + O2  [=] OH + O' ,
        ...                     'id' : 'reaction01', 'products' : {'O' : '1' , 'OH' : '1'}, 
        ...                     'rate_params' : {'A' : 3520000.0, 'E' : 71400.0 , 'b' : -0.7 }, 
        ...                     'rate_type' : 'Arrhenius' , 'reactants' : {'H' : '1' , 'O2' : '1'} , 
        ...                     'reversible': 'no', 'type' : ' Elementary'})
        
        >>> elementary_reaction = ElementaryReaction({'equation' : 'H + O2  [=] OH + O' ,
        ...                     'id' : 'reaction01', 'products' : {'O' : '1' , 'OH' : '1'}, 
        ...                     'rate_params' : {'A' : 3520000.0, 'E' : 71400.0 , 'b' : -0.7 }, 
        ...                     'rate_type' : 'Arrhenius' , 'reactants' : {'H' : '1' , 'O2' : '1'} , 
        ...                     'reversible': 'yes', 'type' : ' Elementary'})
        Traceback (most recent call last):
        ...
        NotImplementedError: The library only deals with irreversible reactions.You have given a reversible reaction.
        """
        self.reaction_properties = reaction_properties
        self.rate_type = self.reaction_properties['rate_type']
        self.rate_params = self.reaction_properties['rate_params']
        self.reactants = self.reaction_properties['reactants']
        self.products = self.reaction_properties['products']
        self.reversible = True if self.reaction_properties['reversible'] == 'yes' else False
        if self.reversible: raise NotImplementedError('The library only deals with irreversible reactions.'
                                        'You have given a reversible reaction.') 

    def __repr__(self):
        """Returns a string containing basic information
         about the Elementary reaction

        RETURNS:
        ========
        str: string
             containing basic information about
             the Elementary reaction
        """
        info = "Reactants: {} \nProducts: {} \nRate Params: {} \nRate Type: {} \nReversible: {}".format(self.reactants, 
            self.products, self.rate_params, self.rate_type, self.reversible)
        return info        
        
    def get_reactants(self):
        """
        Returns a dictionary with reactants as key 
        and the stoichiometric coeff as value for each elementary reaction.

        INPUTS:
        =======
        None

        OUTPUTS:
        ========
        reactants: a dictionary with reactants as key 
        and the stoichiometric coeff as value.

        EXAMPLES:
        =========
        >>> elementary_reaction = ElementaryReaction({'equation' : 'H + O2  [=] OH + O' ,
        ...                     'id' : 'reaction01', 'products' : {'O' : '1' , 'OH' : '1'}, 
        ...                     'rate_params' : {'A' : 3520000.0, 'E' : 71400.0 , 'b' : -0.7 }, 
        ...                     'rate_type' : 'Arrhenius' , 'reactants' : {'H' : '1' , 'O2' : '1'} , 
        ...                     'reversible': 'no', 'type' : ' Elementary'})
        >>> elementary_reaction.get_reactants()
        {'H': '1', 'O2': '1'}
        """
        
        return self.reactants
    
    def get_products(self):
        """
        Returns a dictionary of products as key and the 
        stoichiometric coeff as value for each elementary reaction.

        INPUTS:
        =======
        None

        OUTPUTS:
        ========
        reactants: a dictionary of reactants as key 
        and the stoichiometric product coeff as value.

        EXAMPLES:
        =========
        >>> elementary_reaction = ElementaryReaction({'equation' : 'H + O2  [=] OH + O' ,
        ...                     'id' : 'reaction01', 'products' : {'O' : '1' , 'OH' : '1'}, 
        ...                     'rate_params' : {'A' : 3520000.0, 'E' : 71400.0 , 'b' : -0.7 }, 
        ...                     'rate_type' : 'Arrhenius' , 'reactants' : {'H' : '1' , 'O2' : '1'} , 
        ...                     'reversible': 'no', 'type' : ' Elementary'})
        >>> elementary_reaction.get_products()
        {'O': '1', 'OH': '1'}
        """
        return self.products
    
    def calculate_rate_coefficient(self, T):
        """
        Calculates and returns a rate coeffiecient based on the type of 
        rate coefficeint required

        INPUTS:
        =======
        T : float, 
            Temperature in Kelvin scale,
            Must be positive

        OUTPUTS:
        ========
        rate_coeff : float,
                     rate coefficient based on the type 
                     of rate coefficient required.

        EXAMPLES:
        =========
        >>> elementary_reaction = ElementaryReaction({'equation' : 'H + O2  [=] OH + O' ,
        ...                     'id' : 'reaction01', 'products' : {'O' : '1' , 'OH' : '1'}, 
        ...                     'rate_params' : {'A' : 3520000.0, 'E' : 71400.0 , 'b' : -0.7 }, 
        ...                     'rate_type' : 'Arrhenius' , 'reactants' : {'H' : '1' , 'O2' : '1'} , 
        ...                     'reversible': 'no', 'type' : ' Elementary'})
        >>> elementary_reaction.calculate_rate_coefficient(1000)
        5.2102032610668552
        """

        if self.rate_type:
            if self.rate_type.lower() == 'constant':
                if 'k' in self.rate_params:
                    return self._constant_rate(self.rate_params['k'])
                else:
                    return self._constant_rate()
            else:
                A = self.rate_params['A']
                E = self.rate_params['E']
                b = self.rate_params['b']
                return self._k_arrhenius(A, E, T, b)
        else:
            raise ValueError('No value for `type of rate` passed. '
                             'Pass a value to get the reaction coeff')

    def _constant_rate(self, k = 1.0):
        """
        Returns a constant reaction rate coefficient.

        In zeroth-order reactions, k = constant.

        INPUTS:
        =======
        k: float, default value = 1.0
           Constant reaction rate coefficient

        RETURNS:
        ========
        k: float
           Constant reaction rate coefficient

        Notes
        -----
        Although it would be sensible if input is numeric, no exceptions
        will be raised if this is not the case.

        EXAMPLES:
        =========
        >>> elementary_reaction = ElementaryReaction({'equation' : 'H + O2  [=] OH + O' ,
        ...                     'id' : 'reaction01', 'products' : {'O' : '1' , 'OH' : '1'}, 
        ...                     'rate_params' : {'A' : 3520000.0, 'E' : 71400.0 , 'b' : -0.7 }, 
        ...                     'rate_type' : 'Arrhenius' , 'reactants' : {'H' : '1' , 'O2' : '1'} , 
        ...                     'reversible': 'no', 'type' : ' Elementary'})
        >>> elementary_reaction._constant_rate(5.0)
        5.0
        """
        if k < 0:
            raise ValueError("Constant reaction rate cannot be negative. "
                             "Check the value. ")

        return k

    def _k_arrhenius(self, A, E, T, b = 0.0, R = 8.314):
        """Return a reaction rate coefficient according to the Arrhenius equation.

        The Arrhenius equation relates the rate constant, k, of a chemical
        reaction to parameters A (pre-exponential factor), E (activation
        energy), T (absolute temperature), and b (exponential indicating
        temperature-dependence of pre-exponential factor)::

            k = A T^b exp[ -E / (RT) ]

        When ``b = 0``, the above formula corresponds to the Arrhenius equation.  
        A nonzero value for b gives the modified Arrhenius equation.

        INPUTS:
        =======
        A: float,
           Arrhenius prefactor, Must be positive
        b: float,
           Modified Arrhenius parameter, default value = 0.0
        E: float,
           Activation energy
        T: float,
           Temperature, Must be positive
        R: float, default value = 8.314
           Ideal gas constant

        RETURNS:
        ========
        k: float,
           Arrhenius reaction rate coefficient

        EXAMPLES:
        =========
        EXAMPLES:
        =========
        >>> elementary_reaction = ElementaryReaction({'equation' : 'H + O2  [=] OH + O' ,
        ...                     'id' : 'reaction01', 'products' : {'O' : '1' , 'OH' : '1'}, 
        ...                     'rate_params' : {'A' : 3520000.0, 'E' : 71400.0 , 'b' : -0.7 }, 
        ...                     'rate_type' : 'Arrhenius' , 'reactants' : {'H' : '1' , 'O2' : '1'} , 
        ...                     'reversible': 'no', 'type' : ' Elementary'})
        >>> elementary_reaction._k_arrhenius(3520000.0, 71400.0, 1000.0, -0.7)
        5.2102032610668552
        """
        if A < 0.0:
            raise ValueError("Activation Energy `A` must be positive.")

        if T < 0.0:
            raise ValueError("Temperature `T` (in Kelvin scale) cannot be negative." )

        k_arrhenius = (A * T ** b) * np.exp(-E / (R * T))
        return k_arrhenius



class ReactionSystem():
    """Class for a system of reactions

    Take a list of dictionaries from the ElementaryReaction class. Build stoichiometric coefficient matrices for the 
    reactants and products, and calculate the corresponding progress rates and reaction rates.
    """
    def __init__(self, elementary_reactions, species):
        """Constructor

        INPUTS:
        =======
        elementary_reactions: a list of dictionaries 
                              each element in the list is a dictionary of the information for an elementary reaction
        species:              a list
                              species in the reaction system
        """
        self.elementary_reactions = elementary_reactions
        self.species = species
        self.reactant_coefficients = self.build_reactant_coefficient_matrix()
        self.product_coefficients = self.build_product_coefficient_matrix()

    def __repr__(self):
        """Returns a string containing basic information for the reaction system

        RETURNS:
        ========
        str: string
             Containing information on species and stoichiometric coefficients
        """
        info = "Species: {} \nStoichiometric coefficients of reactants: {} \nStoichiometric coefficients of products: {}".format(self.species, 
            self.reactant_coefficients, self.product_coefficients)
        return info

    def __len__(self):
        """Returns the number of species in the reaction system

        RETURNS:
        ========
        species_len: int
                     the number of species in the reaction system

        EXAMPLES:
        =========
        >>> concs = [1., 2., 1., 3., 1.]
        >>> reader = XMLReader("tests/rxns.xml")
        >>> reaction_system = reader.get_reaction_systems()
        >>> len(reaction_system[0])
        5
        """
        return len(self.species)

    def calculate_progress_rate(self, concs, temperature):
        """Returns the progress rate of a system of irreversible, elementary reactions

        INPUTS:
        =======
        concs:    numpy array of floats 
                  concentration of species
        temperature: numpy array of floats
                     temperatures of the elementary reactions

        RETURNS:
        ========
        progress: numpy array of floats
                  size: num_reactions
                  progress rate of each reaction

        EXAMPLES:
        =========
        >>> concs = [1., 2., 1., 3., 1.]
        >>> reader = XMLReader("tests/rxns.xml")
        >>> reaction_system = reader.get_reaction_systems()
        >>> reaction_system[0].calculate_progress_rate(concs, 300)
        [0.00024002941214766843, 39.005602653448953]
        """
        k = self.get_rate_coefficients(temperature)
        if type(k) is float:
            k = [k]*len(self.reactant_coefficients[0])
        progress = k # Initialize progress rates with reaction rate coefficients
        for jdx, rj in enumerate(progress):
            if rj < 0:
                raise ValueError("k = {0:18.16e}:  Negative reaction "
                                 "rate coefficients are prohibited!".format(rj))
            for idx, xi in enumerate(concs):
                nu_ij = self.reactant_coefficients[idx,jdx]
                if xi  < 0.0:
                    raise ValueError("x{0} = {1:18.16e}:  Negative concentrations are prohibited!".format(idx, xi))
                if nu_ij < 0:
                    raise ValueError("nu_{0}{1} = {2}:  Negative stoichiometric coefficients are prohibited!".format(idx, jdx, nu_ij))
                
                progress[jdx] *= xi**nu_ij
        return progress   

    def calculate_reaction_rate(self, concs, temperature):
        """Returns the reaction rate of a system of irreversible, elementary reactions
        
        INPUTS:
        =======
        concs:    numpy array of floats 
                  concentration of species
        temperature: numpy array of floats
                     temperatures of the elementary reactions

        RETURNS:
        ========
        f: numpy array of floats
           size: num_species
           reaction rate of each specie

        EXAMPLES:
        =========
        >>> concs = [1., 2., 1., 3., 1.]
        >>> reader = XMLReader("tests/rxns.xml")
        >>> reaction_system = reader.get_reaction_systems()
        >>> reaction_system[0].calculate_reaction_rate(concs, 300)
        array([  3.90053626e+01,  -3.90053626e+01,   3.90058427e+01,
                -3.90056027e+01,  -2.40029412e-04])
        """
        nu = self.product_coefficients - self.reactant_coefficients
        rj = self.calculate_progress_rate(concs, temperature)
        return np.dot(nu, rj)

    def get_rate_coefficients(self, temperature):
        """Calculate reaction rate coefficients
        
        INPUTS:
        =======
        temperature: numpy array of floats
                     temperatures of the elementary reactions

        RETURNS:
        ========
        f: numpy array of floats
           reaction rate ooefficients

        EXAMPLES:
        =========
        >>> reader = XMLReader("tests/rxns.xml")
        >>> reaction_system = reader.get_reaction_systems()
        >>> reaction_system[0].get_rate_coefficients(300)
        [0.00024002941214766843, 6.5009337755748255]
        """
        coefficients = [er.calculate_rate_coefficient(temperature) for er
                        in self.elementary_reactions]
        return coefficients

    def build_reactant_coefficient_matrix(self):
        """Build a reactant coefficients matrix for the reaction system

        RETURNS:
        ========
        f: numpy array of floats
           reactant coefficients matrix

        EXAMPLES:
        =========
        >>> reader = XMLReader("tests/rxns.xml")
        >>> reaction_system = reader.get_reaction_systems()
        >>> reaction_system[0].build_reactant_coefficient_matrix()
        array([[ 1.,  0.],
               [ 0.,  1.],
               [ 0.,  0.],
               [ 0.,  1.],
               [ 1.,  0.]])
        """
        mat = np.zeros([len(self.species), len(self.elementary_reactions)])
        for i, reaction in enumerate(self.elementary_reactions):
            dict_react = reaction.get_reactants()
            for j,species in enumerate(self.species):
                mat[j,i] = dict_react.get(species, 0)
        return mat

    def build_product_coefficient_matrix(self):
        """Build a product coefficients matrix for the reaction system

        RETURNS:
        ========
        f: numpy array of floats
           product coefficients matrix

        EXAMPLES:
        =========
        >>> reader = XMLReader("tests/rxns.xml")
        >>> reaction_system = reader.get_reaction_systems()
        >>> reaction_system[0].build_product_coefficient_matrix()
        array([[ 0.,  1.],
               [ 1.,  0.],
               [ 1.,  1.],
               [ 0.,  0.],
               [ 0.,  0.]])
        """
        mat = np.zeros([len(self.species), len(self.elementary_reactions)])
        for i, reaction in enumerate(self.elementary_reactions):
            dict_prod = reaction.get_products()
            for j,species in enumerate(self.species):
                mat[j,i] = dict_prod.get(species, 0)
        return mat


class XMLReader():
    """
    Parser for chemical reaction XML files. Uses `xml.etree`.

    Parameters
    ----------
    xml_file : str
         Path to XML file.

    Attributes
    ----------
    xml_file : str
         Path to XML file.
    root : xml.etree.Element
         Top-level element in parsed tree.

    Methods
    -------
    get_reaction_system()
         Parse all groups of reactions in the XML file.

    Examples
    --------
    >>> reader = XMLReader("tests/rxns.xml")
    >>> reaction_systems = reader.get_reaction_systems()
    """
    def __init__(self, xml_file):
        self.xml_file = xml_file
        xml_tree = ET.parse(xml_file)
        self.root = xml_tree.getroot()

    def _parse_reaction(self, reaction_elt):
        """Collect individual reaction properties in a dictionary.

        The first "rateCoeff" entry found is converted into two items,
        `rate_type` and `rate_params`, the former containing the
        reaction type and the latter being a dictionary of rate
        parameters.

        Parameters
        ----------
        reaction_elt : xml.etree.Element
             A "reaction" entry within a "reactionData"
             entry. Corresponds to an elementary reaction.
        
        Returns
        -------
        properties : dict
             Dictionary of reaction parameters.
        """
        properties = reaction_elt.attrib.copy()

        properties["equation"] = reaction_elt.find("equation").text

        rate_coeff = reaction_elt.find("rateCoeff")
        rate_coeff_child = rate_coeff.getchildren()[0]
        properties["rate_type"] = rate_coeff_child.tag
        properties["rate_params"] = {}
        for child in rate_coeff_child.getchildren():
            properties["rate_params"][child.tag] = float(child.text)

        reactants = reaction_elt.find("reactants").text.split()
        properties["reactants"] = {}
        for reactant in reactants:
            species, coefficient = reactant.split(':')
            properties['reactants'][species] = coefficient

        products = reaction_elt.find("products").text.split()
        properties["products"] = {}
        for reactant in products:
            species, coefficient = reactant.split(':')
            properties['products'][species] = float(coefficient)

        return properties

    def _get_species(self):
        """Return the species involved in the reaction.

        Returns
        -------
        species : list
            A list of strings identifying the species involved in the
            reaction.
        """
        try:
            phase_elt = self.root.find('phase')
            species_array_elt = phase_elt.find('speciesArray')
            species_text = species_array_elt.text
        except AttributeError:
            raise LookupError("Element root>phase>speciesArray")
        species = species_text.split()
        return species

    def get_reaction_systems(self):
        """Parse all groups of reactions in xml file.

        Returns
        -------
        reaction_systems : list
             A list of `ReactionSystem` instances corresponding to
             each "reactionData" entry in the XML file.
        """
        species = self._get_species()
        reaction_systems = []
        for reaction_data in self.root.findall('reactionData'):
            elementary_reactions = []
            for reaction in reaction_data.findall('reaction'):
                reaction_properties = self._parse_reaction(reaction)
                if reaction_properties['type'] != "Elementary":
                    raise NotImplementedError
                elementary_reaction = ElementaryReaction(reaction_properties)
                elementary_reactions.append(elementary_reaction)
            reaction_system = ReactionSystem(elementary_reactions, species)
            reaction_systems.append(reaction_system)

        return reaction_systems    

    def __repr__(self):
        return "XMLReader(%s)" % self.xml_file



if __name__ == "__main__":
    import doctest
    doctest.testmod()


