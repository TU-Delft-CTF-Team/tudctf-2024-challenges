#include <cstring>
#include <iostream>
#include <map>
#include <unordered_set>
#include <utility>
#include <vector>

int populate(std::vector<char>& tree, const char* word, int tree_index, int word_index) {
    if(tree_index >= tree.size() || word_index >= std::strlen(word)) {
        return word_index;
    }

    word_index = populate(tree, word, (tree_index << 1) + 1, word_index);
    word_index = populate(tree, word, (tree_index << 1) + 2, word_index);

    if(word_index < std::strlen(word)) {
        tree[tree_index] = word[word_index++];
    }

    return word_index;
}

void verify(std::vector<char>& tree, int index, std::unordered_set<char> const& leafs_rules, std::map<std::pair<char, char>, char>& nodes_rules) {
    if((index << 1) + 1 >= tree.size()) {
        if(!leafs_rules.contains(tree[index])) {
            tree[index] = 0;
        }

        return;
    }

    verify(tree, (index << 1) + 1, leafs_rules, nodes_rules);
    verify(tree, (index << 1) + 2, leafs_rules, nodes_rules);

    char left = tree[(index << 1) + 1];
    char right = tree[(index << 1) + 2];

    if(nodes_rules[{ left, right }] != tree[index]) {
        tree[index] = 0;
    }
}

int main(int argc, char** argv) {
    if(argc != 2) {
        std::cout << "Usage: " << argv[0] << " <flag>" << std::endl;
        return 0;
    }

    int input_size = std::strlen(argv[1]);
    int tree_size;

    for(tree_size = 1; tree_size < input_size; tree_size <<= 1);

    std::vector<char> tree(tree_size - 1, ' ');

    populate(tree, argv[1], 0, 0);

    // std::unordered_set<char> leafs_rules{ 'T', 'U', 'C', 't', 'r', '3', '_', '0', 'm', '4', '_', 's', 'l', 'H' };
    std::unordered_set<char> leafs_rules{ '0', '3', '4', 'C', 'H', 'T', 'U', '_', 'l', 'm', 'r', 's', 't' };
    std::map<std::pair<char, char>, char> nodes_rules{
        {{'a', '_'}, '&'},
        {{'&', 'L'}, 'l'},
        {{'t', 'e'}, 'L'},
        {{'l', 'H'}, 'e'},
        {{'t', 'r'}, '3'},
        {{'0', 'm'}, 'a'},
        {{'3', '_'}, '4'},
        {{'T', 'U'}, 'D'},
        {{'C', 'T'}, 'F'},
        {{'t', '4'}, '_'},
        {{'_', 's'}, 't'},
        {{'{', 'u'}, 't'},
        {{'3', '4'}, 'u'},
        {{'D', 'F'}, '{'},
        {{'t', 'l'}, '}'}
    };

    verify(tree, 0, leafs_rules, nodes_rules);
    
    if(tree[0] == '}') {
        std::cout << "Good job!" << std::endl;
    } else {
        std::cout << "Try again!" << std::endl;
    }

    // std::cout << tree.size() << ' ' << '"' << std::string(tree.cbegin(), tree.cend()) << '"' << std::endl;

    return 0;
}